Project Charter
This document outlines the plans, features, and technical architecture for the Riskskanner.ai: a risk document identification scanner project that utilizes AI/ML. Make it suitable for standalone, professional-grade web application that automatically scans English-language project documents to identify and highlight potential risks, assumptions, and dependencies, with a future goal of integrating its logic into the Flexi PMS.
Problem Statement
Contract workers, Project managers and stakeholders especially new graduate students that are applying for jobs often struggle to manually identify potential risks, ambiguities, assumptions, and dependencies hidden within lengthy project documents (contracts, proposals, scopes of work). This manual process is time-consuming and prone to human error, leading to unforeseen issues, budget overruns, and project delays.
Scope & Success Criteria
Scope: The MVP is a public-facing web application with no user accounts. It will focus on text extraction, risk analysis, and clear presentation of results.
Success:
The backend API can process a 10-page document and return a response in under 20 seconds.
The decoupled frontend and backend are successfully deployed and communicating in a production environment.
The scanner correctly identifies over 80% of keyword-based risks in a standard test document set.
Team Roles & Responsibilities
Backend Team(AI & API)
Lead: SUN Heng
Responsibility: 
Develop, maintain, and deploy the Python-based backend server.
Build and own the core risk analysis engine.
Implement the logic for extracting text from .pdf and .docx files.
Design, build, and document the REST API that serves the frontend.
Ensure API performance, security, and reliability.
Handle all server-side deployment and infrastructure concerns.
Frontend Team
Lead: Sophea Darika wtfff who is bro?
Responsibility: 
Develop, maintain, and deploy the React-based frontend application.
Create a responsive, intuitive, and visually appealing user interface.
Implement all user-facing features, including file uploads, text inputs, and results displays.
Consume data from the backend API and render it effectively for the user.
Manage the frontend build process and deployment.
Ensure a seamless user experience across different browsers and devices.
Guiding Principle: The API is the Contract
The backend and frontend teams work independently but are connected by the API. The API specification in Section 5 is the single source of truth. The backend guarantees the API will function as described; the frontend guarantees it will consume the API as described. The frontend team can and should use "mock" data matching the API contract to build the entire UI without waiting for the backend to be completed.
Product & Feature Specification (MVP v1.0)
Core User Experience
A user visits the website and is presented with a clean interface to either upload a file or paste text. After submitting, a loading state appears. Once the scan is complete, the results are displayed in a structured, easy-to-read table, highlighting the risk, its category, and the context in which it was found.
MVP Feature List
(BA = Backend, FE = Frontend)
Priority
ID
Feature Description
Owner
Status
Must-Have
F-01
User can paste raw text into a text area.
FE
To Do
Must-Have
F-02
User can select/drag a .docx or .pdf file.
FE
To Do
Must-Have
F-03
A "Scan" button initiates the API call.
FE
To Do
Must-Have
F-04
API endpoint accepts file/text data.
BA
To Do
Must-Have
F-05
Backend extracts text from uploaded files.
BA
To Do
Must-Have
F-06
Backend performs risk analysis on text.
BA
To Do
Must-Have
F-07
API returns a structured JSON response.
BA
To Do
Must-Have
F-08
Frontend displays results in a clear table.
FE
To Do
High
F-09
Frontend is deployed to a public URL (Netlify, Vercel).
FE
To Do
High
F-10
Backend is deployed to a public URL (Heroku, Render).
BA
To Do
Medium
F-11
UI shows a proper loading state during the scan.
FE
To Do
Medium
F-12
UI shows clear error messages returned by the API.
FE
To Do

Technical Architecture & Stack
System Architecture
A decoupled client-server model. The React Frontend is a static application that runs in the user's browser. It communicates with the FastAPI Backend via a REST API over HTTPS.
Backend Technology Stack
Language: Python 3.9+
API Framework: FastAPI
Text Extraction: python-docx, PyMuPDF
Risk Analysis Engine: Python re module (for v1.0)
Deployment: Heroku or Render
Frontend Technology Stack
Framework: React (using Create React App or Vite)
API Communication: Axios
Styling: Tailwind CSS
Deployment: Netlify or Vercel.
The API Contract
This is the definitive contract between the frontend and backend.
Endpoint Definition
URL: POST /scan
Method: POST
Content-Type: multipart/form-data
Request Body Parameters:
file (optional, file): The uploaded .docx or .pdf file.
text (optional, string): The raw pasted text. The backend should give file precedence if both are provided.
Success Response (200 OK)
The API will return a JSON object with a single key, data. data contains a list of risk objects. An empty list signifies no risks were found.
Error Response (4xx/5xx)





Empty Lorem Ipsum
Development Workflow & Next Steps
Kickoff Meeting: All team members review and agree upon this document.
Parallel Development:
Backend Team: Begins by creating the FastAPI server and implementing the /scan endpoint. Use a dummy function that returns the hard-coded "Success Response" from section 5.2. This is called stubbing the API.
Frontend Team: Begins building the UI components in React, using the hard-coded JSON from section 5.2 as mock data. This allows for the entire UI to be built before the backend logic is complete.
Integration: Once the API is stubbed and the initial UI is built, the teams work to integrate them. The frontend replaces its mock data with a real axios call to the backend.
Completion: The backend team replaces the dummy function with the real risk-scanning logic.
Immediate Action Items:
Backend: Set up a new FastAPI project and create the /scan endpoint structure.
Frontend: Set up a new React project and build the main layout with the file uploader and text area components.