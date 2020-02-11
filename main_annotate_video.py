import os
from image_annotator import ImageAnnotator
from video_transformer import VideoTransformer

# Set parameters
PATH_CRED = "./"
PATH_VID = "./video.mp4"		# location video 
DIR_FRAMES = "./frames/"				# directory to store frames (will be created)
PATH_VID_AN = "video_an.mp4"			# name of annotated video
DIR_FRAMES_AN = "./frames_an/"			# directory to store annotated frames (will be created)
VID_FPS = 30

print("running")

# Create objects
img_annotator = ImageAnnotator(PATH_CRED)
video_transf = VideoTransformer(VID_FPS)

# create folder for frames
try:
	os.mkdir(DIR_FRAMES)
except:
	print("Folder " + DIR_FRAMES + " already exists")
	for filename in os.listdir(DIR_FRAMES):
		file_path = os.path.join(DIR_FRAMES, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

try:
	os.mkdir(DIR_FRAMES_AN)
except:
	print("Folder " + DIR_FRAMES_AN + " already exists")
	for filename in os.listdir(DIR_FRAMES_AN):
		file_path = os.path.join(DIR_FRAMES_AN, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

# Turn video into frames
print("Turn video into frames")
video_transf.video_to_frame(PATH_VID, DIR_FRAMES)

# iterate through frames
print("Get informations from images")
for file in os.listdir(DIR_FRAMES):
	if file.endswith(".jpg") or file.endswith(".png"):
		# Get information from images
		img_objects = img_annotator.get_objects(DIR_FRAMES+file, True)

		# Annotate images
		img_annotator.annotate_image(DIR_FRAMES+file, DIR_FRAMES_AN+file, img_objects)

# transform frames to video
print("Transform frames to video")
video_transf.frame_to_video(DIR_FRAMES_AN, PATH_VID_AN)

print("Done!")

