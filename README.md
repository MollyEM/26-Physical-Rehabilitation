<!DOCTYPE html>
<html>
<head>
</head>
<body>

<h1>Using Deep Learning to Provide Feedback for Remote Physical Rehabilitation</h1>
<h2>Team Name: Remote Rehabilitation</h2>
<h3>Purpose</h3>
<p>When patients incorrectly perform physical therapy exercises their doctor suggests following an injury, their recovery time is extended, leading to financial and physical strain. By adjusting a deep learning model that analyzes videos of clients exercising remotely, we can provide real time feedback potentially resulting in improved rehabilitation outcomes. .</p>

<h3>Background</h3>
<a href = https://github.com/avakanski/A-Deep-Learning-Framework-for-Assessing-Physical-Rehabilitation-Exercises> </a>
<a href = https://github.com/CMU-Perceptual-Computing-Lab/openpose></a>
<h3>Product Requirements</h3>
<ul>
  <li>Analyze at least one exercise (Deep Squat) </li>
  <li>Produce an accurate numerical rating</li>
  <li>Be able to analyze videos taken from smart phones</li>
  <li>Provide feedback in a reasonable amount of time</li>
  <li>Analyze at least 100 human skeletal movements</li>
</ul>
<h3>Progress</h3>
<p>Able to extract skeletal joints from .avi videos for each frame by using OpenPose body_25 model.</p>
<p>Preprocessed data for input into neural network model for training</p>
<img src="https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Project%20Learning/Scripts%20with%20Videos/RandomlySelectedSequences.png" alt = "Joint Positions vs Frame Count for Random Episodes​">

<h3>Currently Working On:</h3>
<ul>
  <li>Improving episode split</li>
  <li>Adding more exercises!</li>
</ul>
</body>
</html>








