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
<Motor_Positions>
<highvoltagecmd pos="1.00000" units="mm" description="High Voltage ON OFF Device" type="FLOAT32">1.000000</highvoltagecmd>
<selector_speed pos="3104.60000" units="rpm" description="Velocity Selector speed" type="FLOAT32">3104.600000</selector_speed>
<selector_tilt pos="0.00000" units="deg" description="Velocity Selector angle" type="FLOAT32">0.000000</selector_tilt>
<coll_1 pos="aperture" units="mm" description="SANS Collimator #1" type="FLOAT32">101.288533</coll_1>
<coll_2 pos="open" units="mm" description="SANS Collimator #2" type="FLOAT32">2.134768</coll_2>
<coll_3 pos="open" units="mm" description="SANS Collimator #3" type="FLOAT32">2.136038</coll_3>
<coll_4 pos="open" units="mm" description="SANS Collimator #4" type="FLOAT32">3.410649</coll_4>
<coll_5 pos="open" units="mm" description="SANS Collimator #5" type="FLOAT32">1.610246</coll_5>
<coll_6 pos="open" units="mm" description="SANS Collimator #6" type="FLOAT32">2.521445</coll_6>
<coll_7 pos="open" units="mm" description="SANS Collimator #7" type="FLOAT32">3.342462</coll_7>
<coll_8 pos="open" units="mm" description="SANS Collimator #8" type="FLOAT32">3.120441</coll_8>
<nguides pos="0.00000" units="number" description="Number of guides" type="FLOAT32">0.000000</nguides>
<attenuator_pos pos="open" units="mm" description="Attenuator stage position" type="FLOAT32">52.997100</attenuator_pos>
<beam_trap_x pos="80.00004" units="mm" description="Beamtrap X position (mm)" type="FLOAT32">80.000043</beam_trap_x>
<dcal pos="4.99978" units="mm" description="Detector Calibration Bar (mm)" type="FLOAT32">4.999777</dcal>
<detector_trans pos="1.00000" units="mm" description="Horizontal detector translation (mm)" type="FLOAT32">0.999998</detector_trans>
<sample_det_dist pos="18.50000" units="m" description="Control the distance from the sample to the detector." type="FLOAT32">18.500000</sample_det_dist>
<sample_x pos="-62.69715" units="mm" description="Sample Changer X stage position emag" type="FLOAT32">-62.697154</sample_x>
<trap_y_101mm pos="1.00005" units="mm" description="200mm Beamtrap Y position" type="FLOAT32">1.000049</trap_y_101mm>
<trap_y_25mm pos="1.00005" units="mm" description="25mm Beamtrap Y position" type="FLOAT32">1.000049</trap_y_25mm>
<trap_y_50mm pos="1.00005" units="mm" description="40mm Beamtrap Y position" type="FLOAT32">1.000049</trap_y_50mm>
<trap_y_76mm pos="542.00003" units="mm" description="100mm Beamtrap Y position" type="FLOAT32">542.000034</trap_y_76mm>
</Motor_Positions>
<Parameter_Positions>
<hvsts1 pos="1174.00000" units="V" description="High voltage Power Supply feedback" type="FLOAT32">1174.000000</hvsts1>
<hvsts2 pos="1173.00000" units="V" description="High voltage Power Supply feedback" type="FLOAT32">1173.000000</hvsts2>
<hvsts3 pos="1167.00000" units="V" description="High voltage Power Supply feedback" type="FLOAT32">1167.000000</hvsts3>
<mag_current pos="2.500000" units="A" description="Read Genesys power supply current setpoint." type="FLOAT32">2.500000</mag_current>
</Parameter_Positions>
<Counters>
<time units="sec" description="Counting time." type="FLOAT32">1800.000000</time>
<detector units="counts" description="Detector counts." type="FLOAT32">19033907.000000</detector>
<monitor units="counts" description="Monitor counts." type="FLOAT32">3977251.000000</monitor>
</Counters>
<Data description="Raw counts from detector">
<!--  The detector data is in the form of n rows of m columns.

The type declaration is INT32[n,m].  The form of the data, X, is

X(1,1)  X(1,2)  X(1,3) ... X(1,m)
.
.
.
X(n,1)  X(n,2) X(n,3) ... X(n,m)

For the SANS detector, the (1,1) position is the bottom left corner as seen from the sample position. -->
<Detector type="INT32[192,256]">
0    0    0    0    0    0    0    0    0    2    1    4    4    3    3    3    6    3    4    5    4    3    6    7    4    6    8    10    6    6    5    8    5    1    7    8    4    6    10    5    5    5    5    10    5    8    7    5    8    7    6    9    8    9    9    6    8    2    7    6    4    9    8    5    9    14    4    6    5    5    15    7    7    11    10    11    6    10    4    8    4    9    4    10    4    8    9    9    7    8    9    5    8    12    18    16    11    7    4    18    10    10    11    8    15    6    11    9    16    10    6    11    7    8    9    7    11    8    7    8    10    6    11    18    6    9    6    13    8    12    10    7    6    7    8    4    7    12    10    11    8    7    9    8    10    14    9    10    9    9    6    13    8    7    13    8    8    8    7    8    11    7    5    8    8    8    10    8    5    5    7    5    9    11    7    9    8    6    6    5    5    10    7    6    3    7    12    10    11    7    5    6    6    6    9    8    4    8    4    3    4    8    3    3    3    8    5    5    4    3    7    5    4    9    9    4    3    8    1    5    5    5    7    5    6    1    6    5    3    4    4    5    4    5    4    5    4    6    5    2    4    6    4    3    4    1    0    0    0    0    0    0    0    0    0    0
0    0    0    0    0    0    0    0    0    0    2    4    2    4    2    4    5    3    3    4    1    2    4    7    6    5    6    4    5    8    4    4    8    5    4    5    2    4    6    0    2    3    8    3    5    5    6    5    3    2    4    9    4    6    9    3    5    3    2    3    4    7    3    8    1    5    6    5    2    5    7    4    3    3    5    8    6    5    7    2    8    11    7    6    12    4    9    3    5    7    8    6    4    3    7    11    9    6    6    4    4    6    8    10    4    7    5    6    5    6    7    11    8    8    4    8    7    7    2    5    8    9    5    5    4    0    7    12    8    2    2    5    2    6    9    8    7    1    6    3    5    9    10    11    3    2    8    5    6    4    7    2    5    8    10    4    2    10    7    9    9    5    8    3    6    5    6    5    9    3    9    3    7    5    5    11    6    7    3    2    6    3    7    7    8    4    5    10    4    3    3    5    5    9    3    2    9    6    5    3    2    5    2    2    4    6    7    7    4    2    3    4    4    3    7    0    9    4    4    3    3    4    1    2    5    6    5    2    2    4    3    1    4    6    4    1    4    1    3    1    1    1    4    2    4    0    0    0    0    0    0    0    0    0    0    0
</Detector>
</Data>
</SPICErack>"""

# import cStringIO
# from lxml import etree
# from pprint import pprint 
# f = cStringIO.StringIO(text)
# tree = etree.parse(f)
# find_text = etree.XPath("//text()")
# 
# 
# # and print out the required data
# pprint( {tree.getpath( text.getparent()) : text.getparent().text 
#          for text in find_text(tree) 
#             if text.getparent().text != None and text.getparent().text.strip() != ""} )


TAGS_TO_IGNORE = ["Data"]

from lxml import etree

root = etree.fromstring(text)

notes_to_iter = [node for node in root.getchildren() if node.tag not in TAGS_TO_IGNORE]

#tree = etree.ElementTree(root)

for node in notes_to_iter:
    tree = etree.ElementTree(node)
    for e in node.getiterator():
        if e.text is not None and e.text.strip() != "":
            print tree.getpath(e), '=' , e.text



