<!DOCTYPE html>
<html>
<head>
</head>
<body>

<h1>Using Deep Learning to Provide Feedback for Remote Physical Rehabilitation</h1>
<h2>Team Name: Remote Rehabilitation</h2>
<h3>Purpose</h3>
<p>When patients incorrectly perform physical therapy exercises their doctor suggests following an injury, their recovery time is extended, leading to financial and physical strain. By adjusting a deep learning model that analyzes videos of clients exercising remotely, we can provide real time feedback potentially resulting in improved rehabilitation outcomes.</p>

<h3>Objective</h3>
<p>Train machine learning models to produce feedback for videos of physical therapy exercises taken with a smart phone. 
</p>

<h3>Background</h3>
<p>Link to the original deep learning model developed by our client! This learning model was developed using Vicon and Kinect angular data.
  <a HREF = "https://github.com/avakanski/A-Deep-Learning-Framework-for-Assessing-Physical-Rehabilitation-Exercises" alt = "Deep Learning Framework"> Click Here.</a>
Link to the paper published by Dr. Alexsandar Vakanski and Dr. Min Xian who developed this model.
  <a href = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7032994/" alt = "Paper"> Click Here.</a>
</p>
<p>Link to the Database of collected exercises used for training on our model and of the models proposed above.
  <a href = "https://www.webpages.uidaho.edu/ui-prmd/" alt = "UIPRMD Database" > Click Here</a>
</p>
<p>For extracting the skeletal data from mp4 and avi videos, we used OpenPose. OpenPose is a deep learning model that extracts 25 skeletal joints from a human skeleton from videos or pictures taken by a smart phone. 
<a href = "https://github.com/CMU-Perceptual-Computing-Lab/openpose">OpenPose Git Repository</a></p>

<h3>Product Requirements</h3>
<ul>
  <li>Analyze at least one exercise (Deep Squat) </li>
  <li>Produce an accurate numerical rating</li>
  <li>Be able to analyze videos taken from smart phones</li>
  <li>Provide feedback in a reasonable amount of time</li>
  <li>Analyze at least 100 human skeletal movements</li>
</ul>

<h3>Final Poster Presentation</h3>
<img src = "Final Design Documentation/Expo-2024-Poster-Remote-Rehabilitation.pptx" alt = "Final Poster Presentation">

<h3>Project</h3>
<p>AFter extracting the skeletal information from a video, we scaled the (x,y) postitional data of each joint and centered it on the mean.</p>
<img src="Final Design Documentation/FinalDesignPictures/DSSmoothSeq.jpg" alt = "Joint Positions vs Frame Count for Random Episodes​">
<p>This image depicts 4 randomly selected deep squat sequences. Each line is an x, y, or z joint location from each joint over 40 frames. This data was fed into the model for training</p>

<h4>Final Spatio Temporal Model Training and Testing Outcome</h4>
<img src = "Final Design Documentation/FinalDesignPictures/TandTST.jpg" alt = "Comparison between Predicted Quality and Label​">
<p>The red squares represent the models predicted score, and the green dots are the human assigned score of the accuracy of that squat</p>

<h4>Spatio Temporal Model Training Loss</h4>
<img src = "https://github.com/MollyEM/26-Physical-Rehabilitation/blob/main/Design%20Solution/TrainingLoss.png" alt = "Improved training loss">

<h3>Testing of the Spatio Temporal Model for the Deep Squat Exercise</h3>
<img src = "Final Design Documentation/FinalDesignPictures/CDSTest.jpg" alt = "20 correct form squat accuracy prediction distribution using the Spatio Temporal Model">
<p> 20 correct form squat accuracy prediction distribution using the Spatio Temporal Model. </p>
<img src = "Final Design Documentation/FinalDesignPictures/IDSTst.jpg" alt = "20 incorrect form squat accuracy prediction distribution using the Spatio Temporal Model">
<p>20 incorrect form squat accuracy prediction distribution using the Spatio Temporal Model.</p>
<p>From the images above, we concluded that the Spatio Temporal model that we developed is more accurate in predicting correct form squats but has a high rate of predicting a squat is correct form when analyzing incorrect form of squats.</p>

<h3>Future Work</h3>
<p>We would suggest to include a larger database for training on our machine learning approaches to increase generalizability and accuracy. We would also suggest adding more exercises to the machine learning. Exploring a more detailed skeletal extraction model could also increase the accuracy of the model.</p>
<h3>Final Paper</h3>
<p>For more detail, reference the final paper <a href = "Final Design Documentation/Design Report.docx">here.</a></p>



</html>








