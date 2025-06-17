
const moment = require('moment');

class Platform {
  constructor(name, maxRating = 5000) {
    this.name = name;
    this.maxRating = maxRating;
    this.difficulty = null;
    this.participation = null;
    this.drift = null;
    this.lastUpdate = null;
    this.userRatings = new Map();
    this.historicalStats = [];
  }

  updateStats(difficulty, participation, currentRatings) {
    const ratings = Object.values(currentRatings);
    const avgRating = ratings.length > 0 ? ratings.reduce((a, b) => a + b, 0) / ratings.length : 0;
    
    this.historicalStats.push({
      difficulty,
      participation,
      avgRating,
      timestamp: new Date()
    });

    this.difficulty = difficulty / this.maxRating;
    this.participation = participation;
    this.drift = this._calculateDrift(currentRatings);
    this.lastUpdate = new Date();

    Object.entries(currentRatings).forEach(([userId, rating]) => {
      if (!this.userRatings.has(userId)) {
        this.userRatings.set(userId, new Map());
      }
      this.userRatings.get(userId).set(new Date(), rating);
    });
  }

  _calculateDrift(currentRatings) {
    if (this.historicalStats.length === 0 || Object.keys(currentRatings).length === 0) {
      return 0.0;
    }
    
    const recentStats = this.historicalStats.slice(-5);
    const histAvg = recentStats.reduce((sum, stat) => sum + stat.avgRating, 0) / recentStats.length;
    const currentAvg = Object.values(currentRatings).reduce((a, b) => a + b, 0) / Object.values(currentRatings).length;
    
    return Math.abs(currentAvg - histAvg) / this.maxRating;
  }
}

class User {
  constructor(userId) {
    this.userId = userId;
    this.platformRatings = {};
    this.completedCourses = [];
    this.unifiedRating = 0.0;
    this.courseBonus = 0.0;
    this.totalRating = 0.0;
  }
}

class UnifiedRankingSystem {
  constructor(alpha = 0.5, beta = 0.3, gamma = 0.2, decayLambda = 0.01) {
    this.alpha = alpha;
    this.beta = beta;
    this.gamma = gamma;
    this.decayLambda = decayLambda;
    this.platforms = new Map();
    this.users = new Map();
    this.rawWeights = {};
    this.softmaxWeights = {};
    this.finalWeights = {};
  }

  addPlatform(platformName, maxRating = 5000) {
    this.platforms.set(platformName, new Platform(platformName, maxRating));
  }

  addUser(userId) {
    this.users.set(userId, new User(userId));
  }

  updatePlatformStats(platformName, difficulty, participation, currentRatings) {
    if (!this.platforms.has(platformName)) {
      throw new Error(`Platform ${platformName} not found`);
    }
    
    const platform = this.platforms.get(platformName);
    platform.updateStats(difficulty, participation, currentRatings);

    Object.entries(currentRatings).forEach(([userId, rating]) => {
      if (!this.users.has(userId)) {
        this.addUser(userId);
      }
      this.users.get(userId).platformRatings[platformName] = rating;
    });

    this._calculateWeights();
    this._updateAllRatings();
  }

  _calculateWeights() {
    this.rawWeights = {};
    
    for (const [platformName, platform] of this.platforms) {
      if (platform.difficulty === null || platform.participation === null || platform.drift === null) {
        continue;
      }
      
      const rawWeight = this.alpha * platform.difficulty + 
                       this.beta * platform.participation + 
                       this.gamma * platform.drift;
      this.rawWeights[platformName] = rawWeight;
    }

    // Softmax normalization
    const expWeights = {};
    Object.entries(this.rawWeights).forEach(([platform, weight]) => {
      expWeights[platform] = Math.exp(weight);
    });
    
    const sumExp = Object.values(expWeights).reduce((a, b) => a + b, 0) || 1e-8;
    
    this.softmaxWeights = {};
    Object.entries(expWeights).forEach(([platform, weight]) => {
      this.softmaxWeights[platform] = weight / sumExp;
    });

    // Apply time decay
    this.finalWeights = {};
    for (const [platformName, platform] of this.platforms) {
      if (!platform.lastUpdate) continue;
      
      const deltaT = moment().diff(moment(platform.lastUpdate), 'days');
      this.finalWeights[platformName] = this.softmaxWeights[platformName] * 
                                       Math.exp(-this.decayLambda * deltaT);
    }
  }

  _imputeMissingRating(user, platformName) {
    const validRatings = Object.entries(user.platformRatings)
      .filter(([p, r]) => p !== platformName)
      .map(([p, r]) => r);
    
    if (validRatings.length > 0) {
      return validRatings.reduce((a, b) => a + b, 0) / validRatings.length;
    }
    
    const platform = this.platforms.get(platformName);
    if (platform.historicalStats.length > 0) {
      const recentStats = platform.historicalStats.slice(-3);
      return recentStats.reduce((sum, stat) => sum + stat.avgRating, 0) / recentStats.length;
    }
    
    return platform.maxRating * 0.5;
  }

  _updateAllRatings() {
    for (const user of this.users.values()) {
      let unifiedRating = 0.0;
      let totalWeight = 0.0;
      
      Object.entries(this.finalWeights).forEach(([platformName, weight]) => {
        let rating = user.platformRatings[platformName];
        if (rating === undefined) {
          rating = this._imputeMissingRating(user, platformName);
        }
        unifiedRating += weight * rating;
        totalWeight += weight;
      });
      
      user.unifiedRating = totalWeight > 0 ? unifiedRating / totalWeight : 0;
      user.totalRating = user.unifiedRating;
    }
  }

  getRankings(topN = null) {
    const sortedUsers = Array.from(this.users.values())
      .sort((a, b) => b.totalRating - a.totalRating);
    
    const rankings = sortedUsers.map(user => [
      user.userId,
      user.unifiedRating,
      user.courseBonus,
      user.totalRating
    ]);
    
    return topN ? rankings.slice(0, topN) : rankings;
  }
}

module.exports = { Platform, User, UnifiedRankingSystem };
