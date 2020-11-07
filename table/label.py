import glob

targetPattern = r"/home/yaocong/table/Yolos/*.jpg"
result =glob.glob(targetPattern)
for f in result:
	print(f)
	#print(result,sep='',end='\n',file=open('train.txt','w'))  此格式darknet不接??

