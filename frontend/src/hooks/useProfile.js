import { useState, useEffect } from "react";
import { getUserProfile } from "../services/apiClient";

const defaultProfileData = {
  email: "",
};

export const useProfile = () => {
  const [profileData, setProfileData] = useState(defaultProfileData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await getUserProfile();
        setProfileData(data);
      } catch (err) {
        setError("Failed to load profile.");
      }
      setLoading(false);
    };
    fetchProfile();
  }, []);
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
    loading,
    error,
  };
};
