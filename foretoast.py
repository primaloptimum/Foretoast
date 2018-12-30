#!/usr/bin/python3
import os
import sys
import time
import argparse

def ArgumentsValidation(fileName,Directory,beg):
    if os.path.exists(fileName)==False or os.path.isdir(fileName):
        print("The image file: "+fileName+" doesn't exist")
        exit(1)

    if os.path.exists(Directory) and os.path.isdir(Directory) ==False:
        print(Directory+" is not a directory")
        exit(1)

    FileSize=os.stat(fileName).st_size
    if beg<0 or beg>FileSize:
        print("Invalid beginning")
        exit(1)
    else:
        b=0
        try:
            b=int(b)
        except:
            print("Invalid beginning")
            exit(1)
        global Beginning
        Beginning=b-int(b)%4096

    if os.path.exists(Directory)==False:
        os.makedirs(Directory)
    global file
    file=open(fileName,'rb')


class Chunk(object):
    Chunk=4096

#The Number of the supported file types
NumberOfTypes=6
#Declaring a counter for each type
Data=[0 for i in range(NumberOfTypes)]
#in order [JPG,PDF,GIF,ZIP,TXT,PNG]
StackOfHeaders=[]


def Extraction(file, type, NextHeader):#calls the exraction functions depending on file type.

    ExtractFunctions=[ExtractPDF,ExtractJPG,ExtractGIF,ExtractZIP,ExtractPNG,ExtractTXT]

    if type > len(ExtractFunctions) or type < -1:
        print("Unsupported type")
        return file

    return ExtractFunctions[type](file,NextHeader)

def ExtractJPG(binary,NextHeader):
    if os.path.exists(Directory+"/JPG")==False:
        os.makedirs(Directory+"/JPG")


    extraction=open(Directory+"/JPG/bla"+ str(Data[0]) +".jpg", "wb")

    FootIndex=-1

    while FootIndex==-1:
        size=len(binary)
        if FootIndex==-1:
            for b in range(4095, 0, -1):
                if binary[b]==0:
                    continue

                elif binary[b]==217 and binary[b-1]==255:
                    FootIndex=b

                break

        if FootIndex==-1:
            extraction.write(binary)

        else:
            extraction.write(binary[0:FootIndex+1])
            extraction.close()
            Data[0]+=1
            return

        binary=file.read(Chunk.Chunk)
        if(file.tell()>NextHeader):
            extraction.close()
            os.remove(Directory+"/JPG/bla"+ str(Data[0]) +".jpg")
            Data[0]-=1
            file.seek(NextHeader)
            return

def ExtractPDF(binary,NextHeader):
    if os.path.exists(Directory+"/PDF")==False:
        os.makedirs(Directory+"/PDF")
    extraction=open(Directory+"/PDF/bla"+ str(Data[1]) +".pdf", "wb")

    FootIndex=-1

    while FootIndex==-1:
        size=len(binary)
        if FootIndex==-1:
            for b in range(4095, 0, -1):

                if binary[b]==0 or binary[b]==10:
                    continue
                elif binary[b]==70 and binary[b-1]==79 and binary[b-2]==69 and binary[b-3]==37 and binary[b-4]==37:
                    FootIndex=b
                break

        if FootIndex==-1:
            extraction.write(binary)

        else:
            extraction.write(binary[:FootIndex+1])
            extraction.close()
            Data[1]+=1
            return

        binary=file.read(Chunk.Chunk)
        if(file.tell()>=NextHeader):
            extraction.close()
            os.remove(Directory+"/PDF/bla"+ str(Data[1])+".pdf")
            Data[1]-=1
            file.seek(NextHeader)
            return

def ExtractGIF(binary,NextHeader):
    if os.path.exists(Directory+"/GIF")==False:
        os.makedirs(Directory+"/GIF")
    Last3B=False

    extraction=open(Directory+"/GIF/bla"+ str(Data[2]) +".gif", "wb")

    FootIndex=-1
    while True:
        size=len(binary)
        if FootIndex==-1:
            Last3B=False
            for b in range(4095, 0, -1):
                if binary[b]==59 and Last3B:
                    FootIndex=b
                    break

                if binary[b]!=0:
                    break

                Last3B=True


        if FootIndex==-1:
            extraction.write(binary)

        else:
            extraction.write(binary[:FootIndex+1])
            extraction.close()
            Data[2]+=1
            return

        binary=file.read(Chunk.Chunk)
        if(file.tell()>=NextHeader):
            extraction.close()
            os.remove(Directory+"/GIF/bla"+ str(Data[2]) +".gif")
            Data[2]-=1
            file.seek(NextHeader)
            return

def ExtractZIP(binary,NextHeader):
    if os.path.exists(Directory+"/ZIP")==False:
        os.makedirs(Directory+"/ZIP")
    extraction=open(Directory+"/ZIP/bla"+ str(Data[3]) +".zip", "wb")

    FootIndex=-1

    while FootIndex==-1:
        size=len(binary)
        if FootIndex==-1:

            counter=0
            ZeroPadding=True

            for b in range(4095, 0, -1):
                if counter==20 and ZeroPadding==False:
                    break
                if binary[b]==0:
                    continue
                elif binary[b]==6 and binary[b-1]==5 and binary[b-2]==75 and binary[b-3]==80:
                    FootIndex=b

                counter+=1
                ZeroPadding=False

        if FootIndex==-1:
            extraction.write(binary)

        else:
            extraction.write(binary)
            extraction.close()
            Data[3]+=1
            return

        binary=file.read(Chunk.Chunk)
        if(file.tell()>=NextHeader):
            extraction.close()
            os.remove(Directory+"/ZIP/bla"+ str(Data[3]) +".zip")
            Data[3]-=1
            file.seek(NextHeader)
            return

def ExtractTXT(binary):
    if os.path.exists(Directory+"/TXT")==False:
        os.makedirs(Directory+"/TXT")

    extraction=open(Directory+"/TXT/bla"+ str(Data[4]) +".txt", "wb")

    ZeroPadding=False

    FootIndex=-1
    while True:
        size=len(binary)
        if FootIndex==-1:
            ZeroPadding=False
            for b in range(4095, 0, -1):
                if (binary[b]>31 and binary[b]<127) or (binary[b]>6 and binary[b]<14):
                    FootIndex=b
                    break

                if binary[b]!=0:
                    break

                ZeroPadding=True


        if FootIndex==-1:
            extraction.write(binary)

        else:
            extraction.write(binary[:FootIndex+1])
            extraction.close()
            Data[4]+=1
            return binary

        binary=file.read(Chunk.Chunk)

def ExtractPNG(binary,NextHeader):
    if os.path.exists(Directory+"/PNG")==False:
        os.makedirs(Directory+"/PNG")
    extraction=open(Directory+"/PNG/bla"+ str(Data[5]) +".png", "wb")

    FootIndex=-1

    while FootIndex==-1:
        size=len(binary)
        if FootIndex==-1:
            for b in range(4095, 0, -1):
                if binary[b]==0:
                    continue
                elif binary[b]==130 and binary[b-1]==96 and binary[b-2]==66 and binary[b-3]==174 and binary[b-4]==68 and binary[b-5]==78 and binary[b-6]==69 and binary[b-7]==73 :
                    FootIndex=b
                break

        if FootIndex==-1:
            extraction.write(binary)

        else:
            extraction.write(binary[:FootIndex+1])
            extraction.close()
            Data[5]+=1
            file.seek(NextHeader)
            return

        if(file.tell()>=NextHeader):
            extraction.close()
            os.remove(Directory+"/PNG/bla"+ str(Data[5]) +".png")
            Data[5]-=1
            file.seek(NextHeader)
            return
        binary=file.read(Chunk.Chunk)






def HeaderSearch(binary):
    TXT=False
    if binary[0]==37 and binary[1]==80 and binary[2]==68:#PDF
        StackOfHeaders.append((0,file.tell()-4096))

    elif binary[0]==255 and binary[1]==216 and binary[2]==255:#JPG
        StackOfHeaders.append((1,file.tell()-4096))

    elif binary[0]==71 and binary[1]==73 and binary[2]==70 and binary[3]==56:#GIF
        StackOfHeaders.append((2,file.tell()-4096))

    elif binary[0]==80 and binary[1]==75 and binary[2]==3 and binary[3]==4 and binary[4]==20:#ZIP
        StackOfHeaders.append((3,file.tell()-4096))

    elif binary[0]==137 and binary[1]==80 and binary[2]==78 and binary[3]==71 and binary[4]==13 and binary[5]==10 and binary[6]==26 and binary[7]==10 :#PNG
        StackOfHeaders.append((4,file.tell()-4096))
    else:
        for b in range(10):
            if (binary[b]>31 and binary[b]<127) or (binary[b]>6 and binary[b]<14):
                TXT=True
            else:
                TXT=False
                break
        if TXT==True:
            binary=ExtractTXT(binary)




def main():
    Chunk.counter=0
    first=True
    startTime=time.time()
    print("Scanning the image")
    while True:

        if Chunk.counter%100000==0:
            print("Time Running in Seconds: "+str(int(time.time()-startTime)))
            print(str(int(file.tell()/1000000))+' MBs / '+str(int(FileSize/1000000))+' MBs')
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")

        Chunk.counter+=1


        binary=file.read(Chunk.Chunk)
        size=len(binary)

        if size<4096:
            break
        else:
            HeaderSearch(binary)

    print("")
    print("")
    print("------------------------------------------------------")
    print("Scanning Complete!")
    print("found "+str(len(StackOfHeaders))+" possible files:")

    for i in range(len(StackOfHeaders)):
        print("Trying file number "+str(i+1))
        sys.stdout.write("\033[F")
        file.seek(StackOfHeaders[i][1])
        if i==len(StackOfHeaders)-1:
            Extraction(file.read(4096),StackOfHeaders[i][0],FileSize)
        else:
            Extraction(file.read(4096),StackOfHeaders[i][0],StackOfHeaders[i+1][1])



#Help menu
desc='''
This is a data recovery tool
'''
parser=argparse.ArgumentParser(description=desc)
parser.add_argument('-i',"--image",type=str,metavar="",required=True,help="The disk image you want to recover files form")
parser.add_argument('-b',"--beginning",type=str,metavar="",help="Skip the first N Bs")
parser.add_argument('-d',"--directory",type=str,metavar=""   ,help="choose a path to save the recovered files to")
args=parser.parse_args()



Directory="recovered"
Beginning=0


file=args.image
Directory=args.directory if args.directory!=None else "recovered"
Beginning=int(args.beginning) if args.beginning!=None else 0
ArgumentsValidation(file,Directory,Beginning)





FileSize=file.seek(-1,2)
file.seek(Beginning)

main()

print("")
print("Data Recovery Complete!")
print("")
