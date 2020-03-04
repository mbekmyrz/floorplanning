import xml.etree.ElementTree as ET
import random


class Tile:
    def __init__(self, tile_type):
        self.type = tile_type
        self.x = -1
        self.y = -1
        self.used = False
        self.available = True


class Resource:
    def __init__(self, res_type):
        self.type = res_type
        self.allocated_amount = 0


class DeviceResource(Resource):
    def __init__(self, res_type, amount):
        super().__init__(res_type)
        self.required_amount = 0
        self.total_amount = amount


class ModuleResource(Resource):
    def __init__(self, res_type, amount):
        super().__init__(res_type)
        self.weight = 0
        self.allocated = False
        self.required_amount = amount


class Module:
    def __init__(self, name):
        self.name = name
        self.resources = []
        self.allocated = False
        self.weight = 0
        self.coverage = 0
        self.wastage = 0
        self.tiles = []
        self.x_min = -1
        self.y_min = -1
        self.x_max = -1
        self.y_max = -1

    def update_data(self):
        # update resource data
        for module_resource in self.resources:
            module_resource.allocated_amount = 0
            for tile in self.tiles:
                if tile.type == module_resource.type:
                    module_resource.allocated_amount += 1
            if module_resource.allocated_amount >= module_resource.required_amount:
                module_resource.allocated = True
        # update wastage and coverage
        self.wastage, self.coverage = 0, 0
        for module_resource in self.resources:
            for device_resource in device.resources:
                if module_resource.type == device_resource.type:
                    if module_resource.allocated_amount > module_resource.required_amount == 0:
                        self.wastage += 10000 * module_resource.allocated_amount / device_resource.total_amount
                    elif module_resource.allocated_amount > module_resource.required_amount:
                        self.wastage += (module_resource.allocated_amount - module_resource.required_amount) \
                                        / device_resource.total_amount
                    if not module_resource.required_amount == 0:
                        self.coverage += module_resource.allocated_amount/module_resource.required_amount

    def allocation_check(self):
        for module_resource in self.resources:
            if not module_resource.allocated:
                self.allocated = False
                return
        else:
            self.allocated = True
    
    def overlap_check(self, additional_tile: Tile) -> bool:
        # no tiles
        if len(self.tiles) == 0:
            return False
        # new tile is on the top case
        if self.x_min <= additional_tile.x <= self.x_max and additional_tile.y < self.y_min:
            for i in range(additional_tile.y, self.y_min):
                for j in range(self.x_min, self.x_max + 1):
                    if device.tiles[i][j].used:
                        return True
        # new tile is on the bottom case
        elif self.x_min <= additional_tile.x <= self.x_max and additional_tile.y > self.y_max:
            for i in range(self.y_max + 1, additional_tile.y + 1):
                for j in range(self.x_min, self.x_max + 1):
                    if device.tiles[i][j].used:
                        return True
        # new tile is on the right case
        elif additional_tile.x > self.x_max and self.y_min <= additional_tile.y <= self.y_max:
            for i in range(self.y_min, self.y_max + 1):
                for j in range(self.x_max + 1, additional_tile.x + 1):
                    if device.tiles[i][j].used:
                        return True
        # new tile is on the left case
        elif additional_tile.x < self.x_min and self.y_min <= additional_tile.y <= self.y_max:
            for i in range(self.y_min, self.y_max + 1):
                for j in range(additional_tile.x, self.x_min):
                    if device.tiles[i][j].used:
                        return True
        # new tile is on the diagonal case
        else:
            return True
        # no overlap was found
        return False

    def add_tile(self, additional_tile: Tile):
        # no tiles
        if len(self.tiles) == 0:
            self.tiles.append(additional_tile)
            self.x_min = additional_tile.x
            self.y_min = additional_tile.y
            self.x_max = additional_tile.x
            self.y_max = additional_tile.y
        else:
            # new tile is on the top case
            if self.x_min <= additional_tile.x <= self.x_max and additional_tile.y < self.y_min:
                for i in range(additional_tile.y, self.y_min):
                    for j in range(self.x_min, self.x_max + 1):
                        self.tiles.append(device.tiles[i][j])
            # new tile is on the bottom case
            elif self.x_min <= additional_tile.x <= self.x_max and additional_tile.y > self.y_max:
                for i in range(self.y_max + 1, additional_tile.y + 1):
                    for j in range(self.x_min, self.x_max + 1):
                        self.tiles.append(device.tiles[i][j])
            # new tile is on the right case
            elif additional_tile.x > self.x_max and self.y_min <= additional_tile.y <= self.y_max:
                for i in range(self.y_min, self.y_max + 1):
                    for j in range(self.x_max + 1, additional_tile.x + 1):
                        self.tiles.append(device.tiles[i][j])
            # new tile is on the left case
            elif additional_tile.x < self.x_min and self.y_min <= additional_tile.y <= self.y_max:
                for i in range(self.y_min, self.y_max + 1):
                    for j in range(additional_tile.x, self.x_min):
                        self.tiles.append(device.tiles[i][j])
            # update min, max coordinates
            for tile in self.tiles:
                if self.x_min > tile.x:
                    self.x_min = tile.x
                if self.y_min > tile.y:
                    self.y_min = tile.y
                if self.x_max < tile.x:
                    self.x_max = tile.x
                if self.y_max < tile.y:
                    self.y_max = tile.y


class Device:
    def __init__(self, description_file, requirements_file):
        desc_tree = ET.parse(description_file)
        desc_root = desc_tree.getroot()
        self.rows = int(desc_root.find('rows').text)
        self.columns = int(desc_root.find('columns').text)
        self.resources = []
        self.modules = []
        self.tiles = [[Tile('undefined') for col in range(self.columns)] for row in range(self.rows)]
        self.wastage = 0
        self.allocated = False

        for element in desc_root.find('resources'):
            self.resources.append(DeviceResource(element.attrib['type'], int(element.find('amount').text)))
            for item in element.find('arrangement').text.split(','):
                col = int(item)
                for row in range(self.rows):
                    self.tiles[row][col].x = col
                    self.tiles[row][col].y = row
                    self.tiles[row][col].type = element.attrib['type']

        req_tree = ET.parse(requirements_file)
        req_root = req_tree.getroot()
        for element in req_root:
            module = Module(element.attrib['name'])
            for resource in element:
                module.resources.append(ModuleResource(resource.attrib['type'], int(resource.text)))
            self.modules.append(module)

        for module in self.modules:
            for resource in module.resources:
                if resource.type == "CLB":
                    resource.required_amount /= 20
                elif resource.type == "DSP":
                    resource.required_amount /= 8
                elif resource.type == "BRAM":
                    resource.required_amount /= 4
                if resource.required_amount > int(resource.required_amount):
                    resource.required_amount = int(resource.required_amount) + 1
                resource.required_amount = int(resource.required_amount)

    def print(self):
        for resource in self.resources:
            print(resource.type, resource.amount)
        print('----------')

        for module in self.modules:
            print(module.name)
            for resource in module.resources:
                print(resource.type, resource.required_amount)
            print('--')
        print('----------')

        for i in range(self.rows):
            for j in range(self.columns):
                print(self.tiles[i][j].x, self.tiles[i][j].y, self.tiles[i][j].type)

        print("\nDevice modules schedule:")
        for i in range(len(self.modules)):
            print("\n", i, self.modules[i].name, self.modules[i].weight)
            for j in range(len(self.modules[i].resources)):
                print(j, self.modules[i].resources[j].type, self.modules[i].resources[j].weight)

    def check(self) -> bool:
        for device_resource in self.resources:
            available_resource_amount = device_resource.total_amount
            required_resource_amount = 0
            for module in self.modules:
                for module_resource in module.resources:
                    if module_resource.type == device_resource.type:
                        required_resource_amount += module_resource.required_amount
            # print("Available:", device_resource.type, device_resource.total_amount, "Required:", required_resource_amount)
            if available_resource_amount < required_resource_amount:
                print("Not sufficient resources on the device to allocate all the modules.")
                return False
        print("Resources on the device are sufficient to allocate all the modules.")
        return True

    def schedule(self):
        for module in self.modules:
            for module_resource in module.resources:
                for device_resource in self.resources:
                    if module_resource.type == device_resource.type:
                        module_resource.weight = module_resource.required_amount / device_resource.total_amount
                        module.weight += module_resource.required_amount / device_resource.total_amount

        for i in range(1, len(self.modules)):
            current = self.modules[i]
            j = i - 1
            while j >= 0 and current.weight > self.modules[j].weight:
                self.modules[j + 1] = self.modules[j]
                j -= 1
            self.modules[j + 1] = current

        for module in self.modules:
            for i in range(1, len(module.resources)):
                current = module.resources[i]
                j = i - 1
                while j >= 0 and current.weight > module.resources[j].weight:
                    module.resources[j + 1] = module.resources[j]
                    j -= 1
                module.resources[j + 1] = current

    def update_tiles(self, module: Module):
        # update tiles usage
        for tile in module.tiles:
            self.tiles[tile.y][tile.x].used = True
            
    def check_resource_amount(self):
        for device_resource in self.resources:
            device_resource.allocated_amount = 0
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.tiles[i][j].type == device_resource.type and self.tiles[i][j].used:
                        device_resource.allocated_amount += 1
            device_resource.required_amount = 0
            for module in self.modules:
                for module_resource in module.resources:
                    if module_resource.type == device_resource.type:
                        if module_resource.allocated_amount < module_resource.required_amount:
                            device_resource.required_amount = module_resource.required_amount - module_resource.allocated_amount
            if device_resource.required_amount > device_resource.total_amount - device_resource.allocated_amount:
                return False
            return True

    def find_next_tile(self, module: Module, type) -> Tile:
        if not self.check_resource_amount():
            return None
        elif len(module.tiles) == 0:
            tile = random.choice(random.choice(self.tiles))
            trials = 0
            while not tile.type == type or tile.used or not tile.available and trials < 20:
                tile = random.choice(random.choice(self.tiles))
                trials += 1
            if trials == 20:
                return None
            return tile
        else:
            free_tiles = []
            # top case
            try:
                tile = self.tiles[module.y_min - 1][module.x_min]
                if tile.type == type and not tile.used and tile.available and not module.overlap_check(tile):
                    free_tiles.append(tile)
            except IndexError:
                pass
            # bottom case
            try:
                tile = self.tiles[module.y_max + 1][module.x_max]
                if tile.type == type and not tile.used and tile.available and not module.overlap_check(tile):
                    free_tiles.append(tile)
            except IndexError:
                pass
            # right case
            x = module.x_max + 1
            while x < self.columns:
                tile = self.tiles[module.y_max][x]
                if tile.type == type and not tile.used and tile.available and not module.overlap_check(tile):
                    free_tiles.append(tile)
                    break
                x += 1
            # left case
            x = module.x_min - 1
            while x >= 0:
                tile = self.tiles[module.y_min][x]
                if tile.type == type and not tile.used and tile.available and not module.overlap_check(tile):
                    free_tiles.append(tile)
                    break
                x -= 1
            # no free tile was found
            if len(free_tiles) == 0:
                return None
            # we found free tiles, and now choose the tile with least wastage and highest coverage
            temp_modules = []
            for tile in free_tiles:
                new_module = module
                new_module.add_tile(tile)
                new_module.update_data()
                temp_modules.append(new_module)
            choice = temp_modules[0]
            for i in range(1, len(temp_modules)):
                if temp_modules[i].wastage < choice.wastage or \
                        (temp_modules[i].wastage == choice.wastage and temp_modules[i].coverage > choice.coverage):
                    choice = temp_modules[i]
                    print(temp_modules[i].wastage, temp_modules[i].coverage)
                    print(choice.wastage, choice.coverage)
            return free_tiles[temp_modules.index(choice)]

    def allocation_check(self):
        for module in self.modules:
            if not module.allocated:
                self.allocated = False
                return
        else:
            self.allocated = True

    def update_wastage(self):
        self.wastage = 0
        for modules in self.modules:
            self.wastage += modules.wastage

    def allocate(self):
        for module in self.modules:
            while not module.allocated:
                print("\n", module.name, module.weight)
                for module_resource in module.resources:
                    while not module_resource.allocated:
                        tile = self.find_next_tile(module, module_resource.type)
                        if tile is None:
                            print("No free tile")
                            return
                        module.add_tile(tile)
                        device.update_tiles(module)
                    print(module_resource.type, "allocated:", module_resource.required_amount,
                          module_resource.allocated_amount)
                module.allocation_check()

        print("")
        for module in self.modules:
            if module.allocated:
                print(module.name, "is allocated")


device_choices = []

for i in range(10):
    print("Trial " + str(i) + " started:")
    device = Device('description.xml', 'requirements.xml')
    # try again if it could not allocate all the modules
    while not device.allocated:
        device = Device('description.xml', 'requirements.xml')
        if device.check():
            device.schedule()
            device.allocate()
        device.allocation_check()
    device.update_wastage()
    device_choices.append(device)
    print("Trial " + str(i) + " finished.")

best = device_choices[0]
for device in device_choices:
    if best.wastage > device.wastage:
        best = device
print(device_choices.index(best))







