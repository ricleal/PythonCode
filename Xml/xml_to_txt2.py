import lxml.etree as ET

text = """<SPICErack SPICE_version="1.7" filename="HiResSANS_exp3_scan0011_0001.xml" start_time="2015-07-23 15:11:54" end_time="2015-07-23 15:42:05">
<Header>
<Instrument>HiResSANS</Instrument>
<Reactor_Power type="FLOAT32">85.000000</Reactor_Power>
<Experiment_Title>ipts 14323 high entropy alloys</Experiment_Title>
<Experiment_number type="INT32">3</Experiment_number>
<Command>scan n=0 preset time 1800</Command>
<Builtin_Command>scan n 0 preset time 1800</Builtin_Command>
<Users>Lou Santodonato</Users>
<Local_Contact>KCL LDS</Local_Contact>
<Scan_Number type="INT32">11</Scan_Number>
<Scan_Title>bar1 p1 Al1.3CoCrN 2.5 A scat</Scan_Title>
<Sample_Name></Sample_Name>
<Sample_Changer></Sample_Changer>
<Sample_Thickness units="cm" type="FLOAT32">0.000000</Sample_Thickness>
<Sample_CountRate type="FLOAT32">2209.583889</Sample_CountRate>
<Transmission>False</Transmission>
<Transmission_for_Scan type="INT32">-1</Transmission_for_Scan>
<Detector_Sensitivity_Run_Number type="INT32">0</Detector_Sensitivity_Run_Number>
<Beam_Blocked_Run_Number type="INT32">0</Beam_Blocked_Run_Number>
<Empty_Run_Number type="INT32">0</Empty_Run_Number>
<Number_of_X_Pixels type="INT32">192</Number_of_X_Pixels>
<Number_of_Y_Pixels type="INT32">192</Number_of_Y_Pixels>
<x_mm_per_pixel type="FLOAT32">5.152200</x_mm_per_pixel>
<y_mm_per_pixel type="FLOAT32">5.146200</y_mm_per_pixel>
<beam_center_x_pixel type="FLOAT32">0.000000</beam_center_x_pixel>
<beam_center_y_pixel type="FLOAT32">0.000000</beam_center_y_pixel>
<absolute_intensity_constant type="FLOAT32">0.000000</absolute_intensity_constant>
<source_aperture_size type="FLOAT32">20.000000</source_aperture_size>
<sample_aperture_size type="FLOAT32">2.500000</sample_aperture_size>
<beamtrap_diameter type="FLOAT32">0.000000</beamtrap_diameter>
<source_distance type="FLOAT32">17210.200000</source_distance>
<sample_to_flange type="FLOAT32">285.000000</sample_to_flange>
<sample_aperture_to_flange type="FLOAT32">285.000000</sample_aperture_to_flange>
<tank_internal_offset type="FLOAT32">749.000000</tank_internal_offset>
<wavelength type="FLOAT32">8.000000</wavelength>
<wavelength_spread type="FLOAT32">0.150000</wavelength_spread>
<Comment>none</Comment>
<ImagePath>Images/HiResSANS_exp3_scan0011_0001.png</ImagePath>
</Header>
</SPICErack>"""

def removeNS(tag) :
    if tag.find('}') == -1 :
        return tag
    else:
        return tag.split('}', 1)[1]
        
def linearize(el, path):

    # Print text value if not empty
    if el.text is not None:
        text = el.text.strip()
    else:
        print ""
        return
    if text == "":
        print path
    else:

        # Several lines ?
        lines = text.splitlines()
        if len(lines) > 1:
            lineNb = 1
            for line in lines:
                print path + "[line %d]=%s " % (lineNb, line)
                lineNb += 1
        else:
            print path + "=" + text

    # Print attributes
    for name, val in el.items():
        print path + "/@" + removeNS(name) + "=" + val

    # Counter on the sibbling element names
    counters = {}

    # Loop on child elements
    for childEl in el:

        # Remove namespace
        tag = removeNS(childEl.tag)

        # Tag name already encountered ?
        if counters.has_key(tag):
            counters[tag] += 1
            # Number it
            numberedTag = tag + "[" + str(counters[tag]) + "]"
        else:
            counters[tag] = 1
            numberedTag = tag

        # Print child node recursively
        linearize(childEl, path + '/' + numberedTag)

root = ET.fromstring(text)
linearize(root, "//Header")
