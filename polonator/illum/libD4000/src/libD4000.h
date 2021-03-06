/* libD4000.h  
Formerly D4000_usb.h, DDC4000Ctl.h and RegisterDefines.h
Original copyright by Texas Instruments (info below)
Ported to Linux (and other *nix) via libusb0.1 with permission from TI 
by Dr. Daniel Levner, Church Lab, Harvard Medical School
Copyright Daniel Levner & Texas Instruments, Inc. (c) 2009

Original header:
///////////////////////////////////////////////////////////////////////
//
//            Copyright: Texas Instruments, Inc. (c) 2008
//
//                   TI Proprietary Information
//                         Internal Data
//
//   DESIGN NAME      DDC4000
//
//   FILE NAME        DDC4000_usb.h 
//
//   DESCRIPTION      DDC4000_usb.cpp Header File
//
//   Engineer:        Benjamin Lee
//
///////////////////////////////////////////////////////////////////////
*/


#define DMD_USB_idVendor 0x0451
#define DMD_USB_idProduct 0xaf31

#define DMD_USB_EP_BULK_OUT 0x2		/* Endpoint 2, bulk OUT transfer */
#define	DMD_USB_EP_BULK_IN 0x06		/* Endpoint 86, bulk IN transfer -- EP 6 | USB_ENDPOINT_IN */
#define	DMD_USB_EP_FPGA_PROG 0x8	/* Endpoint 8, bulk OUT FPGA programming */

#define DMD_EZUSB_DRIVER_VERSION_FAKE (0x00010000 + 30)	/* version 1.30 */

#ifndef D4000_USB_BIN	/* set firmware directory */
#define D4000_USB_BIN "/libD4000-1.0/firmware/D4000_usb.bin"
#endif /* D4000_USB_BIN */


#ifdef __cplusplus
extern "C"
{
#endif
	int libD4000_init(void);

	short int libD4000_GetNumDev(void);
	int libD4000_GetDescriptor(int* Array, short int DeviceNum);
	short libD4000_GetFirmwareRev(short int DeviceNumber);
	long libD4000_GetDriverRev(short int DeviceNumber);
	unsigned int libD4000_GetDLLRev(void);
	short int libD4000_GetUsbSpeed(short int DeviceNumber);
	int libD4000_program_FPGA(unsigned char *write_buffer, long write_size, short int DeviceNumber); /* was UCHAR *write_buffer */

	short libD4000_LoadControl(short DeviceNumber);
	short libD4000_ClearFifos(short DeviceNumber);
	int libD4000_LoadData(unsigned char* RowData,long length, int is1080p, short DeviceNumber); /* was UCHAR *RowData, bool is1080p */
	short libD4000_SetBlkMd(short value, short DeviceNumber);
	short libD4000_GetBlkMd(short DeviceNumber);
	short libD4000_SetBlkAd(short value, short DeviceNumber);
	short libD4000_GetBlkAd(short DeviceNumber);
	short libD4000_SetRST2BLKZ(short value, short DeviceNumber);
	short libD4000_GetRST2BLKZ(short DeviceNumber);
	short libD4000_SetRowMd(short value, short DeviceNumber);
	short libD4000_GetRowMd(short DeviceNumber);
	short libD4000_SetRowAddr(short value, short DeviceNumber);
	short libD4000_GetRowAddr(short DeviceNumber);
	short libD4000_SetSTEPVCC(short value, short DeviceNumber);
	short libD4000_GetSTEPVCC(short DeviceNumber);
	short libD4000_SetCOMPDATA(short value, short DeviceNumber);
	short libD4000_GetCOMPDATA(short DeviceNumber);
	short libD4000_SetNSFLIP(short value, short DeviceNumber);
	short libD4000_GetNSFLIP( short DeviceNumber);
	short libD4000_SetWDT(short value, short DeviceNumber);
	short libD4000_GetWDT(short DeviceNumber);
	short libD4000_SetPWRFLOAT(short value, short DeviceNumber);
	short libD4000_GetPWRFLOAT(short DeviceNumber);
	short libD4000_SetEXTRESETENBL(short value, short DeviceNumber);
	short libD4000_GetEXTRESETENBL(short DeviceNumber);
	short libD4000_SetGPIO(short value, short DeviceNumber);
	short libD4000_GetGPIO(short DeviceNumber);
	short libD4000_GetDMDTYPE(short DeviceNumber);
	short libD4000_GetDDCVERSION(short DeviceNumber);

	long libD4000_GetFPGARev(short int DeviceNumber);
	short libD4000_GetRESETCOMPLETE(int waittime, short int DeviceNumber);
	short libD4000_SetGPIORESETCOMPLETE(short int DeviceNumber);
#ifdef __cplusplus
}
#endif



/*
// Defines transfered over from DDC4000Ctl.h
*/

#ifndef LIBD4000_NO_DDC4000CTL_TRANSFER


#ifndef DDC4000CTL_REV

#define D4000_VERSION_CODE 0xAB020000		/* code that is embedded in the FPGA firmware to designate a D4000 */

#define SIZE_OF_XGA 98304
#define SIZE_OF_1080P 259200

#define DMD_1080P 1
#define DMD_XGA	  0

#define BLOCKSPERLOAD1080P 2		/* Must be a mulitple of 14 and no greater than 7 */
#define XGABLOCKSPERLOAD 5		/* Can be 3 or 5 */

/*D4000 USB Register Adresses*/
#define D4000_ADDR_DMDTYPE		0x0010
#define	D4000_ADDR_DDCVERSION		0x0011
#define D4000_ADDR_BLKMD		0x0017
#define D4000_ADDR_BLKAD		0x0018
#define D4000_ADDR_ROWMD		0x0014
#define D4000_ADDR_ROWAD		0x0015
#define D4000_ADDR_CTL1			0x0003
#define D4000_ADDR_CTL2			0x0016
#define	D4000_ADDR_GPIO			0x0019
#define D4000_NUMROWLOADS		0x0020
#define D4000_RESET_COMPLETE		0x0021
#define D4000_GPIORESETFLAG		0x0022

/*D4000 USB Control register 0x03 bits*/
#define D4000_CTLBIT_WRITEBLOCK	0x0001
#define D4000_CTLBIT_RESETCMLPT 0x0008
#define D4000_CTLBIT_CLEARFIFOS	0x0010

/*D4000 USB Control register 0x16 bits*/
#define	D4000_CTLBIT_STEPVCC	0x0001
#define D4000_CTLBIT_COMPDATA	0x0002
#define D4000_CTLBIT_NSFLIP	0x0004
#define D4000_CTLBIT_WDT	0x0008
#define D4000_CTLBIT_PWRFLOATZ	0x0010
#define D4000_CTLBIT_EXTRESET	0x0020
#define	D4000_CTLBIT_RST2BLKZ	0x0040

/*D4000 Define Block modes and Row Modes*/
#define D4000_BLKMD_NOOP	0
#define D4000_BLKMD_CLBLK   	1
#define D4000_BLKMD_RSTBLK	2
#define D4000_BLKMD_11		3
#define D4000_ROWMD_NOOP	0
#define D4000_ROWMD_INC		1
#define D4000_ROWMD_SET		2
#define D4000_ROWMD_SETPNT	3

#define DMD_ALLBLOCKS 17  /* giving this to LoadDMD() does a global write */

#endif /* ifndef DDC4000CTL_REV */



/*
// definitions for functions transferred from DDC4000Ctl.cpp
*/

/* Data which DDC4000Ctl stores per device */
typedef struct DeviceData_struct
{
	/*short BlkMd;
	short BlkAd;
	short RST2BLKZ;
	short RowMd;
	short RowAddr;
	short STEPVCC;
	short COMPDATA;
	short NSFLIP;
	short WDT;
	short PWRFLOAT;
	short EXTRESETENBL;
	short GPIO;
	short THRESHOLD;*/

	int m_bAllowMessageBoxes;   /* was bool m_bAllowMessageBoxes */
	/*bool m_bFullBuffer;*/

	int DMDType;	
	int DMDWidth;
	int DMDHeight;
	int DMDTotalBlocks;
	int DMDRowsPerBlock;
	int DMDBytesPerRow;
	int DMDSizeinBytes;
} DeviceData_type;



#ifdef __cplusplus
extern "C"
{
#endif
	short libD4000_Clear(short BlockNum, short DoReset, short DeviceNumber);
	short libD4000_FloatMirrors(short DeviceNumber);
	short libD4000_LoadToDMD(unsigned char *m_FrameBuff, short BlockNum, short DoReset, short DeviceNumber); /* was UCHAR *m_FrameBuff */
	short libD4000_Reset(short BlockNum, short DeviceNumber);
	short libD4000_DownloadAppsFPGACode(const char *FileName, short DeviceName); /* was LPCTSTR *FileName */
	short libD4000_ConnectDevice(short DeviceNum, const char *SrcFile); /* was LPCTSTR SrcFile */
	short libD4000_AllowMessages(short value, short DeviceNumber);
	int libD4000_IsDeviceAttached(short DeviceNumber); /* was BOOL libD4000_...() */
	short libD4000_GetResetComplete(long waittime, short DeviceNumber);
	
	DeviceData_type libD4000_GetDeviceData(short DeviceNumber);
#ifdef __cplusplus
}
#endif


#endif /* LIBD4000_NO_DDC4000CTL_TRANSFER */

