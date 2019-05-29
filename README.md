# Assignments for Workflow & Process Modelling 

## **Assignment 1**

Polygon intersection function

- GetCapabilities: https://gisedu.itc.utwente.nl/student/s6039782/gpw/wps.py?service=wps&request=GetCapabilities

- DescribeProcess: https://gisedu.itc.utwente.nl/student/s6039782/gpw/wps.py?service=wps&request=DescribeProcess&identifier=polygon_wps_intersection

- Execute: https://gisedu.itc.utwente.nl/student/s6039782/gpw/execute_assign1.py

- Steps: 

    1. *polygon_wps_intersection.py*

        The title, description, paramaters and outputs are first defined in this file which enables the *wps.py* file to recognize this WPService.  
        The *execute()* function is then implemented to perform the intersection.

    2. *polygon_intersection.xml*

        Two polygon examples (JSON format) are used as inputs in the xml to test the WPS.
    
    3. *execute_assign1.py*  

        Read *polygon_intersection.xml* and perform the functionality.

## **Assignment 2**

- Execute: https://gisedu.itc.utwente.nl/student/s6039782/gpw/execute_assign2.py

- Steps:  
    1. *assignment2.xml*  
        
        Process chain:  

        gs:Centroid -> gs:BufferFeatureCollection -> gs:IntersectionFeatureCollection -> gs:Length  
        Length ( Intersection ( Buffer ( Centroid ) ) )

    2. *execute_assign2.py*  

        All neighbourhood are obtained through WFS and corresponding names are extracted. The name is inserted into the XML file through string formatting.  

        Due to time cost, only three neighbourhoods are used in calculation (which turn out to have no intersection with existing streets data).
    
## **Assignment 3**

The workflow for Assignment 2 is shown in *workflow.jpg*. The WorkflowAPP output is stored as *s6039782_assign3.json*.
