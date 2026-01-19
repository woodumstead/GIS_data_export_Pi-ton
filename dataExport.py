
import arcpy

# -------------------------------------------------
# USER INPUTS – EDIT THESE
# -------------------------------------------------

# 1) Your structure layer / feature class
# If 'structure' is a layer in your MXD, just use "structure"
# Otherwise, use the full path to the feature class in the geodatabase
structure_fc = "structure"   # or r"C:\path\to\your\gdb.gdb\structure"

# 2) Field names for latitude and longitude EXACTLY as they appear
lat_field = "latitude"
lon_field = "longitude"

# 3) ID field to include in Excel (change this to your real ID field if needed)
# Examples: "STRUCTURE_ID", "POLE_ID", "STRUCTURE", etc.
id_field = "OBJECTID"   # <-- change if you have a better unique ID

➡️➡️➡️➡️# 4) Output Excel file
out_excel = r"C:\temp\structure_lat_long.xlsx"   # make sure this folder exists ⬅️⬅️⬅️⬅️

# -------------------------------------------------
# MAIN LOGIC – YOU SHOULDN'T NEED TO EDIT BELOW
# -------------------------------------------------

arcpy.env.overwriteOutput = True

print("Using feature class / layer: {}".format(structure_fc))

# Check that fields exist
fields = [f.name for f in arcpy.ListFields(structure_fc)]
missing = []
for f in [id_field, lat_field, lon_field]:
    if f not in fields:
        missing.append(f)

if missing:
    raise ValueError("These fields were not found in {}: {}".format(structure_fc, ", ".join(missing)))

# Build a table view with only the fields we care about
field_list = [id_field, lat_field, lon_field]
field_str = ";".join(field_list)

temp_view = "structure_view_tmp"
if arcpy.Exists(temp_view):
    arcpy.Delete_management(temp_view)

arcpy.MakeTableView_management(structure_fc, temp_view, "", "", field_str)
print("Created temporary table view with fields: {}".format(field_list))

# Export to Excel
arcpy.TableToExcel_conversion(temp_view, out_excel)

print("Export complete!")
print("Excel file created at: {}".format(out_excel))
