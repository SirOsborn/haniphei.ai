import { useState } from "react";

const defaultProfileData = {
  firstName: "John",
  lastName: "Doe",
  email: "john.doe@example.com",
  userType: "freelancer",
};

export const useProfile = () => {
  const [profileData, setProfileData] = useState(defaultProfileData);
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [isEditingProfile, setIsEditingProfile] = useState(false);

  const updateProfile = (field, value) => {
    setProfileData((prev) => ({ ...prev, [field]: value }));
  };

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfilePhoto(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const startEditing = () => {
    setIsEditingProfile(true);
  };

  const cancelEditing = () => {
    setIsEditingProfile(false);
    // In a real app, you would reset to saved data here
  };

  const saveProfile = () => {
    setIsEditingProfile(false);
    // In a real app, you would save to backend here
  };

  return {
    profileData,
    profilePhoto,
    isEditingProfile,
    updateProfile,
    handlePhotoUpload,
    startEditing,
    cancelEditing,
    saveProfile,
  };
};
