# Style Brush
Style Brush is a complete application built on Python that gives users freedom to choose how to style their images. The idea is to build
an application that allows users to style their images as per their wish and finally receive a custom painting to capture the moment instantly, similar to a photo-booth but with more user input.

## Overview
The users can capture an image at the same moment, or instead upload a previously chosen image. The application then runs on eight different style transfer models corresponding to eight painting styles. The eight stylized images are then presented to the user as choices on an interactive user interface, where the user can draw on their image to choose an area to be styled. Once the user makes a selection, a mask is generated for the area chosen, blurred slightly so that the merging between two styles isn’t too sharp and then the chose n style is applied. The user then has the option to go back and continue styling other parts of the image with some of the other styles as per their wish. If not, they can exit the process, upon which the final image is passed through the super resolution model, which outputs a final up-scaled high resolution image that is ready for the user to print.

![alt text](https://github.com/priyanka1706/Style-Brush/blob/master/Working.jpg)
Complete flow of processes

## Modules
### Style Transfer
We use the approach by Johnson et al. to produce multiple styled output images for an input image as it can produce 8 images in less than 5 seconds and the images are visually appealing. Further Ulyanov et al. introduced Instance Normalization which significantly improves image quality. Hence, we combine these approaches to do style transfer in our application

### Interactive Interface
The scribble user interface is built using Tkinter on Python, to give the user freedom to choose as many styles as they like on varying regions, how many ever times they would prefer. The region coordinates are passed on to build a mask that is blurred using a 25x25 Gaussian blur, so that individual styles merge together smoothly. The mask is then used to implement the style on the previous image to present to the user. This gives a final amalgamation of styles that looks pleasing to the eye. 

### Super Resolution
After comparing the results for quality, detail and speed amongst multiple super resolution approaches, finally for the software the implementation of ESRGAN, the work by Wang et al. was chosen. The ESRGAN is a generative adversarial network which was built with inspiration from the work by Ledig et al., with a few deviations, which leads to more detail in the final result. Three changes are done, which can be summarized as a change in the network architecture to remove Batch Normalization layers and replace the blocks
by Residual-in-Residual Dense Blocks (RRDBs), to replace the discriminator in the SRGAN with a Relativistic Discriminator, and to use perceptual loss to get more realistic images. 

![alt text](https://github.com/priyanka1706/Style-Brush/blob/master/UI.jpg)
Complete flow of processes

## References
-  Johnson, Justin, Alexandre Alahi, and Li Fei-Fei. "Perceptual losses for real-time style transfer and
super-resolution." European conference on computer vision. Springer, Cham, 2016.
- Ulyanov, Dmitry, Andrea Vedaldi, and Victor Lempitsky. "Instance normalization: The missing
ingredient for fast stylization." arXiv preprint arXiv:1607.08022 (2016).
- Wang, Xintao, et al. "Esrgan: Enhanced super-resolution generative adversarial networks."
Proceedings of the European Conference on Computer Vision (ECCV). 2018.
- Ledig, Christian, et al. "Photo-realistic single image super-resolution using a generative adversarial
network." Proceedings of the IEEE conference on computer vision and pattern recognition. 2017.
