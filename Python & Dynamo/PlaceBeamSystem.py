import clr

# Import Revit Services
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import ItemFactoryBase

# Get the current Revit document
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Input: Excel file path, level, and beam type data
excel_data = IN[0]  # Full path to the Excel file
beam_type_name = IN[1]  # Beam family type (e.g., 'W12x35')
level_name = IN[2]  # Level where beams will be placed

# Get the beam type from the Revit document by name
beam_type = None
beam_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsElementType()

if beam_type is None:
	beam_type = beam_types.FirstElement()
	
# Collect all levels in the project
levels_collector = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Levels)\
    .WhereElementIsNotElementType()

# Find the level by name
matched_level = None

for level in levels_collector:
	if level.Name == level_name:
		matched_level = level
		break

if matched_level is None:
	matched_level = levels_collector.FirstElement()

# Create beams from Excel data
result = ""

TransactionManager.Instance.EnsureInTransaction(doc)

lines = []

#Iterate through the rows in Excel and place beams
for row in range(len(excel_data)):
	try:
		is_available = True
		
		for col in range(len(excel_data[0])):
			if excel_data[row][col] is None:
				is_available = False
				result += str(row)+ " The data is not accuraccy \n"
				break
	
		if is_available:
			startX = float(excel_data[row][0])
			startY = float(excel_data[row][1])
			endX = float(excel_data[row][2])
			endY = float(excel_data[row][3])
			
			result += str(startX) + ", " + str(startY) + ", " + str(endX) + ", " + str(endY)
			
			z = 3000 #matched_level.Elevation
			
			#start_point = XYZ(startX, startY, z)  # X, Y, Z from Excel
			#end_point = XYZ(endX, endY, z)  # X, Y, Z from Excel
			start_point = XYZ(0, 0, 0)
			end_point = XYZ(10, 0, 0)
			
			
			# Place beam (line element)
			if not beam_type.IsActive:
				beam_type.Activate()
				
			result += "Level Elevation is " + str(matched_level.Elevation)
			
			# Create the beam as a structural element
			line = Line.CreateBound(start_point, end_point)
			
			result += "Line's length = " + str(line.Length)
			
			beam = doc.Create.NewFamilyInstance(line, beam_type, matched_level, 0)
			
			if beam is not None:
				result += str(row) + " beam is created \n"
			else:
				result += str(row) + " beam is failed to create \n"

			TransactionManager.Instance.TransactionTaskDone()

	except Exception as e:
		result += str(row) + " error is ocurred while creating beam \n"
		result += str(e)+ "\n"
		continue
		TransactionManager.Instance.ForceCloseTransaction()
		
#Output: List of created beams
OUT = result
#OUT = lines