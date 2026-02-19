using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.XR.iOS;
using System.Linq;
using System;
using System.Runtime.InteropServices;
using Unity.iOS.Multipeer;
using Unity.iOS.Multipeer.Native;

public class BLECentralManager : MonoBehaviour
{
    private bool _isScanning = false;
    private List<BLEPeripheralDevice> _peripheralDevices = new List<BLEPeripheralDevice>();

    public Text statusText;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize the central manager and set the delegate
        BLECentral.Initialize();
        BLECentral.SetDelegate(this);

        // Start scanning for peripherals
        BLECentral.ScanForPeripherals();

        // Update the status text
        statusText.text = "Scanning for peripherals...";
    }

    // Update is called once per frame
    void Update()
    {
        // Check if the central manager is scanning
        if (_isScanning)
        {
            // Update the status text
            statusText.text = "Scanning for peripherals...";
        }
        else
        {
            // Update the status text with the number of discovered peripherals
            statusText.text = "Discovered " + _peripheralDevices.Count + " peripheral(s)";
        }
    }

    // This method is called when a peripheral device is discovered
    public void DidDiscoverPeripheral(BLEPeripheralDevice peripheralDevice)
    {
        // Add the peripheral device to the list
        _peripheralDevices.Add(peripheralDevice);

        // Log the discovered device
        Debug.Log("Discovered peripheral device: " + peripheralDevice.Name);

        // Update the status text
        statusText.text = "Discovered " + _peripheralDevices.Count + " peripheral(s)";
    }

    // This method is called when the central manager finishes scanning for peripherals
    public void DidFinishScanningForPeripherals()
    {
        // Update the scanning flag
        _isScanning = false;

        // Log the number of discovered peripherals
        Debug.Log("Discovered " + _peripheralDevices.Count + " peripheral(s)");

        // Update the status text with the number of discovered peripherals
        statusText.text = "Discovered " + _peripheralDevices.Count + " peripheral(s)";
    }

    // This method is called when an error occurs while scanning for peripherals
    public void DidFailToScanForPeripheralsWithError(string error)
    {
        // Log the error
        Debug.LogError("Failed to scan for peripherals: " + error);

        // Update the status text with the error message
        statusText.text = "Error: " + error;
    }
}
