Option Explicit

Dim filePath : filePath = "C:\output\"
Dim fileExtention : fileExtention = ".txt"
Dim fileDir


Dim count : count = 1

fileDir = filePath & count
fileDir = fileDir + fileExtention

Dim textone : textone = CreateObject("htmlfile").ParentWindow.ClipboardData.GetData("text")
	Do While count <5


		Dim texttwo : texttwo = CreateObject("htmlfile").ParentWindow.ClipboardData.GetData("text")
		if StrComp(textone, texttwo) = 0 then

		else
			count = count + 1
			fileDir = filePath & count
			fileDir = fileDir + fileExtention



			Dim objStream
			Set objStream = CreateObject("ADODB.Stream")
			objStream.CharSet = "utf-8"
			objStream.Open
			objStream.WriteText texttwo
			objStream.SaveToFile fileDir, 2
			textone = texttwo
		end if
	Loop
