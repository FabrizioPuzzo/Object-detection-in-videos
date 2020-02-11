import io
import os
import sys
import cv2
import random

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

class ImageAnnotator():

	def __init__(self, path_cred=''):

		# Set credentials
		self.path_cred = path_cred
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_cred

		# Instantiates a client
		self.client = vision.ImageAnnotatorClient()
		self.list_used_labels = []

		# Set fix colors for labels 
		self.list_used_labels.append(['Car', (0, 0, 255)]) #Red
		self.list_used_labels.append(['Bus', (0, 0, 255)])
		self.list_used_labels.append(['Van', (0, 0, 255)])
		self.list_used_labels.append(['Truck', (0, 0, 255)])

		self.list_used_labels.append(['Tire', (255, 255, 255)])
		self.list_used_labels.append(['Wheel', (255, 255, 255)])

		self.list_used_labels.append(['Person', (0, 255, 0)]) #Green

		self.list_used_labels.append(['Building', (255, 0, 0)]) #Blue

		# set parameters for rectangle
		self.thickness_rect = 2

		# set parameters for text
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.font_scale = 1
		self.line_type = 2



	def get_objects(self, path_img, print_data):

		""" 
		Annonates image at location path_img returns objects in detected in the image
		args:
			path_img = string
			print_data = bool - prints object data if true
		""" 

		# The name of the image file to annotate
		file_name = os.path.join(
			os.path.dirname(__file__),
			path_img)

		# Loads the image into memory
		with io.open(file_name, 'rb') as image_file:
			content = image_file.read()

			image = types.Image(content=content)
			objects = self.client.object_localization(
				image=image).localized_object_annotations

		if print_data:
			print('Number of objects found: {}'.format(len(objects)))
			for object_ in objects:
				print('\n{} (confidence: {})'.format(object_.name, object_.score))
				print('Normalized bounding polygon vertices: ')
				for vertex in object_.bounding_poly.normalized_vertices:
					print(' - ({}, {})'.format(vertex.x, vertex.y))
		return objects

	def annotate_image(self, path_img, path_img_an, img_objects):
		# read image
		img = cv2.imread(path_img)
		for object_ in img_objects:
			# get vertices
			vertices = []
			for vertex in object_.bounding_poly.normalized_vertices:
				vertices.append((int(vertex.x * img.shape[1]), int(vertex.y* img.shape[0])))

			# Set color for annotation
			color = None
			for label in self.list_used_labels:
				if label[0] == object_.name:
					color = label[1]
			if color is None:
				# Append label with color to list
				self.list_used_labels.append([object_.name,
					(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))])

			# Draw rectangle
			img_an = cv2.rectangle(img, vertices[0] , vertices[2], color, self.thickness_rect)

			# generate string
			str_text = '{0} - {1:.2f}'.format(object_.name, object_.score)

			# put text on the image
			cv2.putText(img_an ,str_text, vertices[0], self.font, self.font_scale, color, self.line_type)


		# save image
		cv2.imwrite(path_img_an, img_an)



