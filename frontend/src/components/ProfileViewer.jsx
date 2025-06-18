import React, { useState, useEffect } from "react";

const ProfileViewer = () => {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userName, setUserName] = useState("Profile Viewer");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/data/sample.json");
        if (!response.ok) {
          throw new Error("Failed to fetch JSON data");
        }
        const data = await response.json();
        setProfileData(data);
        setUserName(data.user_info.name || "Profile Viewer");
        document.title = `${data.user_info.name || "User"}'s Profile`;
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="text-center text-gray-600">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600">Error: {error}</div>;
  }

  const skipItems = [
    "category",
    "desired roles",
    "computer scientist",
    "credentials",
    "bachelor's degree",
  ];

  const courses = profileData.completed_courses
    .filter(
      (course) =>
        course.title &&
        course.certificate_url &&
        !skipItems.some((item) => course.title.toLowerCase().includes(item))
    )
    .reduce((unique, course) => {
      if (!unique.find((c) => c.title === course.title)) {
        unique.push(course);
      }
      return unique;
    }, []);

  const {
    total_bonus_points,
    average_bonus_points,
    max_bonus_points,
    course_count,
  } = profileData.profile_metrics;

  return (
    <div className="bg-white shadow-lg rounded-lg p-6 max-w-md w-full mx-auto">
      <div className="flex flex-col items-center mb-6 border-b pb-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          {profileData.user_info.name || "Unknown User"}
        </h1>
        {profileData.user_info.location && (
          <p className="text-md text-gray-500 mb-1">
            📍 {profileData.user_info.location}
          </p>
        )}
        {profileData.user_info.profile_url && (
          <a
            href={profileData.user_info.profile_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm"
          >
            View Coursera Profile
          </a>
        )}
      </div>

      <p className="text-lg text-gray-600 mb-4">
        Courses Completed:{" "}
        <span className="font-semibold">{courses.length}</span>
        {course_count !== courses.length &&
          ` (Profile reports: ${course_count})`}
      </p>

      <h2 className="text-xl font-semibold text-gray-700 mb-2">
        Completed Courses:
      </h2>
      <ul className="list-disc pl-5 space-y-3 mb-6">
        {courses.map((course, index) => (
          <li key={index} className="text-gray-600">
            <div>
              <span className="font-medium">{course.title}</span>
              {course.institution && (
                <p className="text-sm text-gray-500 mt-1">
                  {course.institution}
                  {course.completion_date && ` • ${course.completion_date}`}
                </p>
              )}
            </div>
          </li>
        ))}
      </ul>

      <h2 className="text-xl font-semibold text-gray-700 mb-2">
        Profile Metrics:
      </h2>
      <div className="text-gray-600 bg-gray-50 p-4 rounded-md">
        <div className="flex justify-between items-center mb-2 border-b pb-2">
          <span className="text-gray-700">Total Bonus Points</span>
          <span className="font-semibold text-blue-600">
            {total_bonus_points}
          </span>
        </div>
        <div className="flex justify-between items-center mb-2 border-b pb-2">
          <span className="text-gray-700">Average Bonus Points</span>
          <span className="font-semibold text-blue-600">
            {average_bonus_points}
          </span>
        </div>
        <div className="flex justify-between items-center mb-2 border-b pb-2">
          <span className="text-gray-700">Max Bonus Points</span>
          <span className="font-semibold text-blue-600">
            {max_bonus_points}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-700">Course Count (Reported)</span>
          <span className="font-semibold text-blue-600">{course_count}</span>
        </div>
      </div>

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-500">
          {userName}'s Profile • Last Updated: {new Date().toLocaleDateString()}
        </p>
      </div>
    </div>
  );
};

export default ProfileViewer;
