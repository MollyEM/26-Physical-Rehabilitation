<!DOCTYPE html>
<html>
<head>
</head>
<body>

<h1>Using Deep Learning to Provide Feedback for Remote Physical Rehabilitation</h1>
<h2>Team Name: Remote Rehabilitation</h2>
<h3>Purpose</h3>
<p>When patients incorrectly perform physical therapy exercises their doctor suggests following an injury, their recovery time is extended, leading to financial and physical strain. By adjusting a deep learning model that analyzes videos of clients exercising remotely, we can provide real time feedback potentially resulting in improved rehabilitation outcomes.</p>

<h3>Background</h3>
<p>Link to Original Deep Learning Model Developed by our Client! This learning model was developed using Vicon and Kinect angular data.
  <a HREF = "https://github.com/avakanski/A-Deep-Learning-Framework-for-Assessing-Physical-Rehabilitation-Exercises" alt = "Deep Learning Framework"> Click Here.</a>
Link to the paper published by Dr. Alexsandar Vakanski and Dr. Min Xian who developed this model.
  <a href = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7032994/" alt = "Paper"> Click Here.</a>
</p>
<p>Link to the Database of collected exercises used for training on our model.
  <a href = "https://www.webpages.uidaho.edu/ui-prmd/" alt = "UIPRMD Database" > Click Here</a>
</p>
<a href = "https://github.com/CMU-Perceptual-Computing-Lab/openpose">Openpose Git Repository</a>
<h3>Product Requirements</h3>
<ul>
  <li>Analyze at least one exercise (Deep Squat) </li>
  <li>Produce an accurate numerical rating</li>
  <li>Be able to analyze videos taken from smart phones</li>
  <li>Provide feedback in a reasonable amount of time</li>
  <li>Analyze at least 100 human skeletal movements</li>
</ul>

<h3>OpenPose</h3>
<p>We used OpenPose deep learning model to extract skeletal joints from 2D videos.</p>
<p> Insert Animation Here</p>

<h3>Progress</h3>
<p>Able to extract skeletal joints from .avi videos for each frame by using OpenPose body_25 model</p>
<p>Preprocessed data for input into neural network model for training</p>
<img src="https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Project%20Learning/Scripts%20with%20Videos/RandomlySelectedSequences.png" alt = "Joint Positions vs Frame Count for Random Episodes​">
<img src = "https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Project%20Learning/Scripts%20with%20Videos/Prediction_Acc_graphs.png" alt = "Comparison between Predicted Quality and Label​">
<p>Improved Sequence data from Smoothing Algorithm and Episode Split</p>
<img src = "https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Final%20Design%20Documentation/Smoothed%20Sequences.png" alt = "Improved Joint Positions vs Frame Count for Random Sequences">

<p>Improved Training Loss</p>
<img src = "https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Design%20Solution/TrainingLoss.png" alt = "Improved training loss">

<p>Improved Training Vs Testing Predictions</p>
<img src = "https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Design%20Solution/TrainingVsTesting.png" alt = "Improved Training Vs Testing Predictions">

<h3>Currently Working On:</h3>
<ul>
  <li>Improving episode split to have more accurate sequences for training</li>
  <li>Analyzing single episode videos uploaded by the user and producing an accuracy score by using the model to predict score</li>
  <li>Adding more exercises!</li>
</ul>
</body>
</html>








