import clr
# Import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point

# Input: Excel file path, level, and beam type data
excel_data = IN[0]  # Full path to the Excel file
start_point = []
result = ""

#Iterate through the rows in Excel and place beams
cols = 3
for row in range(len(excel_data)):
	try:
		is_available = True
		
		if row == 0:
			continue
		
		for col in range(cols):
			if excel_data[row][col] is None:
				is_available = False
				result += str(row)+ " The data is not accuraccy \n"
				break
	
		if is_available:
			x = float(excel_data[row][0])
			y = float(excel_data[row][1])
			z = float(excel_data[row][2])
			
			start_point.append(Point.ByCoordinates(x, y, z))

	except Exception as e:
		result += str(e)+ "\n"
		continue
		
#Output: List of created beams
OUT = start_point