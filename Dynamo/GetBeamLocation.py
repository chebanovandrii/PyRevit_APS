excel_data = [["Start X", "Start Y", "End X", "End Y"], ["3000", "1500", "6000", "1500"]]

for row in range(len(excel_data)):
  try:
    is_available = True
    for col in range(len(excel_data[0])):
      if excel_data[row][col] is None:
        is_available = False
        break
    if is_available:
      startX = float(excel_data[row][0])
      startY = float(excel_data[row][1])
      endX = float(excel_data[row][2])
      endY = float(excel_data[row][3])
      print("x0 = %s, y0 = %s, x1 = %s, y1 = %s" % (startX, startY, endX, endY))
  except Exception as e:
    continue

