# Import necessary modules
import clr

# Import Revit Services
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

# Import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Level

# Get the current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Input: Level name to search for
level_name = IN[0]  # Input comes from Dynamo

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

# Output the matched level or None if not found
OUT = matched_level
