import os
import path 
import sys

def run_all(content_img, folder):
	#content_img='orig3.jpg'
	#folder = 'set3'
	models=['horses','trees','blue_trees','sick_child','candy','mosaic','udnie','rain_princess']

	if not os.path.exists('images/output-images/'+folder):
		os.mkdir('images/output-images/'+folder)

	count=1
	for i in models:
		content_str='images/content-images/'+content_img
		model_str='saved_models/'+i+'.pth'
		output_str='images/output-images/'+folder+'/'+str(count)+'-'+i+'.jpg'
		temp= "python neural_style/neural_style.py eval --content-image='"+content_str+ "' --model='"+model_str+"'  --output-image='"+output_str+ "'  --cuda 0"
		#print(temp)
		count+=1
		os.system(temp)

	print("All styles created!")
