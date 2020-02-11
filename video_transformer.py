import cv2
import os
import re
import numpy

class VideoTransformer():

	def __init__(self, fps=30):
		self.fps = fps

	def video_to_frame(self, path_video, dir_frames):

		vidcap = cv2.VideoCapture(path_video)
		success,image = vidcap.read()
		count = 0
		while success:
			cv2.imwrite(dir_frames + "/frame_" + str(count).zfill(10) + ".jpg", image)     # save frame as JPEG file      
			success,image = vidcap.read()
			#print('Read a new frame: ', success)
			count += 1


	def frame_to_video(self, dir_frames, path_video, fps):
		num_img = []
		images = []
		for img in os.listdir(dir_frames):
			if img.endswith(".png") or img.endswith(".jpg"):
				# using List comprehension + isdigit() +split() 
				# getting numbers from string  
				data = img.split("_")
				data = data[1].split(".")
				num = data[0]
				#print(num)
				num_img.append(num)
				images.append(img)

		sorted_numbers = numpy.argsort(num_img)
		images_sorted = []
		#print(images)
		for i in range(len(images)):
			images_sorted.append(images[sorted_numbers[i]])

		frame = cv2.imread(os.path.join(dir_frames, images_sorted[0]))
		height, width, layers = frame.shape
		fourrc = cv2.VideoWriter_fourcc(*'MP4V')
		video = cv2.VideoWriter(path_video, fourrc, fps, (width, height))

		for image in images_sorted:
			frame = cv2.imread(os.path.join(dir_frames, image))
			video.write(frame)

		cv2.destroyAllWindows()
		video.release()