from ctypes import *
from ctypes.wintypes import *
import win32process, win32ui, win32gui, win32api

windll.kernel32.SetConsoleTitleW("https://github.com/binary")
if not win32gui.FindWindow(None, "Stardew Valley") != 0:
    win32api.MessageBox(0, "stardew valley needs to be open for the program to work", "error")
    exit()

PID = win32process.GetWindowThreadProcessId(win32ui.FindWindow(None, "Stardew Valley").GetSafeHwnd())[1]
OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory
CloseHandle = windll.kernel32.CloseHandle
CoreBaseAddress = 0
ProcessHandle = OpenProcess(0x1F0FFF, False, int(PID))

Modules = win32process.EnumProcessModules(ProcessHandle)
for Address in Modules:
    Name = str(win32process.GetModuleFileNameEx(ProcessHandle, Address))
    if Name.find("coreclr.dll") != -1:
        CoreBaseAddress = Address
        print("[!] found coreclr.dll [" + hex(CoreBaseAddress) + "]")

OffsetAddress = CoreBaseAddress + 0x004AC108
Offsets = [0xB0, 0x1CC, 0x18, 0x360, 0xA8C]

Buffer = c_uint64()
ReadProcessMemory(ProcessHandle, c_uint64(OffsetAddress), byref(Buffer), sizeof(Buffer), None)
AddressBuffer = Buffer.value
ReadProcessMemory(ProcessHandle, c_uint64(AddressBuffer + Offsets[0]), byref(Buffer), sizeof(Buffer), None)

for i in range(1, 4):
    ReadProcessMemory(ProcessHandle, c_uint64(Buffer.value + Offsets[i]), byref(Buffer), sizeof(Buffer), None)

Address = Buffer.value + Offsets[4]
print("[!] stamina found [" + hex(Address) + "]")

def GetStamina():
    Buffer = c_float()
    ReadProcessMemory(ProcessHandle, c_uint64(Address), byref(Buffer), sizeof(Buffer), None)
    return Buffer.value

def UpdateStamina(Value):
    Buffer = c_float()
    WriteProcessMemory(ProcessHandle, c_uint64(Address), byref(c_float(Value)), sizeof(c_float(Value)), byref(Buffer))

while True:
    if GetStamina() != 0 and GetStamina() < 200:
        print("[!] recharging [" + str(int(GetStamina())) + "] -> [270]")
        UpdateStamina(270)
    else:
        if GetStamina() == 0:
            win32api.MessageBox(0, "stardew valley needs to be open for the program to work", "error")
            exit()
