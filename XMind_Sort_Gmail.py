
import xmind
import xmindparser
 
#Open Connection to Gmail
#Read Email Subject and Content to determine Career Path category
#Move Emails into Labels By Career Path category

##LOAD XMIND WORKBOOK DOCUMENT
OpportunityOutline = xmind.load(r"C:\Users\Froap\iCloudDrive\iCloud~net~xmind~brownieapp\Career\Career_Path_Titles.xmind")

##IDENTIFY PRIMARY XMIND WORKBOOK SHEET
PrimarySheet = OpportunityOutline.getPrimarySheet()
SheetTitle = PrimarySheet.getTitle()
print("Current Sheet Name is:",SheetTitle)

#TOPIC
RootTopic = PrimarySheet.getRootTopic()
print(RootTopic)
print("Title:",RootTopic.getTitle())
rt = RootTopic.getSubTopics()
print(RootTopic.getTextContent())


# Open the XMind file
workbook = xmind.load(r"C:\Users\Froap\iCloudDrive\iCloud~net~xmind~brownieapp\Career\Opportunity_Outlines.xmind")


# Get the root topic
root_topic = workbook.getPrimarySheet().getRootTopic()

# Get the first subtopic of the root topic
subtopic = root_topic.getSubTopics()[0]

# Get the text of the subtopic
text = subtopic.getTitle()

# Print the text of the subtopic
print(text)







