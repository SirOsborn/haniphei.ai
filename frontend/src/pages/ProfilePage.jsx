import React from "react";
import { USER_TYPES } from "../constants";

const ProfilePage = ({ profileData, profilePhoto, isEditingProfile, onUpdate, onPhotoUpload, onStartEdit, onCancel, onSave }) => {
  return (
    <main className="max-w-3xl mx-auto px-8 py-12">
      <div className="glass-card">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold text-white">Account Information</h2>
          {!isEditingProfile && (
            <button onClick={onStartEdit} className="btn-secondary text-sm">
              Edit Profile
            </button>
          )}
        </div>

        <div className="flex flex-col md:flex-row gap-8">
          {/* Profile Picture */}
          <div className="flex flex-col items-center gap-3">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white text-3xl font-bold shadow-lg overflow-hidden">
              {profilePhoto ? (
                <img
                  src={profilePhoto}
                  alt="Profile"
                  className="w-full h-full object-cover"
                />
              ) : (
                <span>
                  {profileData.firstName.charAt(0)}
                  {profileData.lastName.charAt(0)}
                </span>
              )}
            </div>
            {isEditingProfile && (
              <div>
                <input
                  type="file"
                  id="photo-upload"
                  accept="image/*"
                  onChange={onPhotoUpload}
                  className="hidden"
                />
                <label
                  htmlFor="photo-upload"
                  className="btn-secondary text-xs py-1.5 px-3 cursor-pointer inline-block"
                >
                  Upload Photo
                </label>
              </div>
            )}
          </div>

          {/* Profile Form */}
          <div className="flex-1 space-y-5">
            {/* First Name & Last Name */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  First Name
                </label>
                <input
                  type="text"
                  value={profileData.firstName}
                  onChange={(e) => onUpdate("firstName", e.target.value)}
                  disabled={!isEditingProfile}
                  className="glass-input disabled:opacity-60 disabled:cursor-not-allowed"
                />
              </div>
              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  Last Name
                </label>
                <input
                  type="text"
                  value={profileData.lastName}
                  onChange={(e) => onUpdate("lastName", e.target.value)}
                  disabled={!isEditingProfile}
                  className="glass-input disabled:opacity-60 disabled:cursor-not-allowed"
                />
              </div>
            </div>

            {/* Email Address */}
            <div>
              <label className="block text-white text-sm font-semibold mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={profileData.email}
                disabled
                className="glass-input disabled:opacity-60 disabled:cursor-not-allowed"
              />
              <p className="text-gray-300 text-xs mt-1">
                Email cannot be changed
              </p>
            </div>

            {/* User Type */}
            <div>
              <label className="block text-white text-sm font-semibold mb-2">
                User Type
              </label>
              <select
                value={profileData.userType}
                onChange={(e) => onUpdate("userType", e.target.value)}
                disabled={!isEditingProfile}
                className="glass-input disabled:opacity-60 disabled:cursor-not-allowed capitalize"
              >
                {USER_TYPES.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Action Buttons */}
            {isEditingProfile && (
              <div className="flex gap-3 pt-4">
                <button onClick={onSave} className="btn-primary flex-1">
                  Save Changes
                </button>
                <button onClick={onCancel} className="btn-secondary flex-1">
                  Cancel
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
};

export default ProfilePage;
