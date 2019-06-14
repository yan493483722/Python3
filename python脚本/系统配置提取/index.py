import wmi
import platform

def sys_version():
    c = wmi.WMI()

    # 操作系统版本，版本号，32位/64位
    print('\n------------------------OS------------------------:')
    sys = c.Win32_OperatingSystem()[0]
    print(sys.Caption, sys.BuildNumber, sys.OSArchitecture)

    # CPU类型 CPU内存
    print('\n------------------------CPU------------------------')
    processor = c.Win32_Processor()[0]
    print(processor.Name.strip())
    Memory = c.Win32_PhysicalMemory()[0]
    print('CPU缓存: ',end="")
    print(int(Memory.Capacity) // 1048576, 'M')


    #内存
    print('\n------------------------内存------------------------')
    totalMemSize = 0
    for memModule in c.Win32_PhysicalMemory():
        totalMemSize += int(memModule.Capacity)
    print("Memory Capacity: %.2fMB" % (totalMemSize / 1048576))

    # 硬盘名称，硬盘剩余空间，硬盘总大小
    print('\n------------------------DISK------------------------')
    for disk in c.Win32_LogicalDisk(DriveType=3):
        print(disk.Caption, 'free:', int(disk.FreeSpace) // 1048576, 'M\t', 'All:', int(disk.Size) // 1048576, 'M')



    print('\n----------------------网卡配置----------------------')
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        print("网卡名称: %s" % interface.Description)
        print("MAC: %s" % interface.MACAddress)
        for ip_address in interface.IPAddress:
            print("\tIP: %s" % ip_address)




    # BIOS版本 生产厂家 释放日期
    print('\n----------------------BIOS----------------------')
    bios = c.Win32_BIOS()[0]
    print(bios.Version)
    print(bios.Manufacturer)
    print(bios.ReleaseDate)

    def TestPlatform():
        print("----------Operation System--------------------------")
        # Windows will be : (32bit, WindowsPE)
        # Linux will be : (32bit, ELF)
        print(platform.architecture())

        # Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
        # Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
        print(platform.platform())

        # Windows will be : Windows
        # Linux will be : Linux
        print(platform.system())

        print("--------------Python Version-------------------------")
        # Windows and Linux will be : 3.1.1 or 3.1.3
        print(platform.python_version())


sys_version()


#linux  直接读取/proc