import xlsxwriter
import main

for device in main.device_choices:
    workbook = xlsxwriter.Workbook('graphics_' + str(main.device_choices.index(device)) + "-" + str(device.wastage) + '.xlsx')
    worksheet = workbook.add_worksheet('Cells')
    worksheet.set_column(0, device.columns, 0.7)
    clb_format = workbook.add_format({'bg_color': '#4A73BE'})
    dsp_format = workbook.add_format({'bg_color': '#7EAA55'})
    bram_format = workbook.add_format({'bg_color': '#66389B'})
    clb_format.set_font_size(9)
    dsp_format.set_font_size(9)
    bram_format.set_font_size(9)
    clb_format.set_border(1)
    dsp_format.set_border(1)
    bram_format.set_border(1)

    allocated_format = [workbook.add_format({'bg_color': '#fffc54'}), workbook.add_format({'bg_color': '#b45651'}),
                        workbook.add_format({'bg_color': '#deedf2'}), workbook.add_format({'bg_color': '#fd9956'}),
                        workbook.add_format({'bg_color': '#62abc3'})]

    for each_format in allocated_format:
        each_format.set_font_size(9)
        each_format.set_border(1)

    for i in range(device.rows):
        for j in range(device.columns):
            index = " (" + str(i) + "," + str(j) + ") "
            if device.tiles[i][j].type == "CLB":
                worksheet.write(i, j, 'C' + index, clb_format)
            elif device.tiles[i][j].type == "DSP":
                worksheet.write(i, j, 'D' + index, dsp_format)
            elif device.tiles[i][j].type == "BRAM":
                worksheet.write(i, j, 'B' + index, bram_format)

    k = 0
    for module in device.modules:
        if k == len(allocated_format):
            k = 0
        for tile in module.tiles:
            index = " (" + str(tile.y) + "," + str(tile.x) + ") "
            if tile.type == "CLB":
                worksheet.write(tile.y, tile.x, 'C' + index + module.name, allocated_format[k])
            elif tile.type == "DSP":
                worksheet.write(tile.y, tile.x, 'D' + index + module.name, allocated_format[k])
            elif tile.type == "BRAM":
                worksheet.write(tile.y, tile.x, 'B' + index + module.name, allocated_format[k])
        k += 1

    # 0. yellow, #fffc54 - module 3
    # 1. red, #b45651 - module 2
    # 2. blue, #deedf2 - module 1
    # 3. orange, #fd9956 - module


    workbook.close()
