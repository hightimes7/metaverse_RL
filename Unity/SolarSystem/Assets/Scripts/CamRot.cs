using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CamRot : MonoBehaviour
{
    float yangle;
    // Start is called before the first frame update
    void Start()
    {
        yangle = transform.localEulerAngles.y;
        Debug.Log("initial angle " + yangle);
    }

    // Update is called once per frame
    void Update()
    {        
        float hv = Input.GetAxis("Mouse X");
        transform.Rotate(0.0f, hv, 0.0f);
        Debug.Log("hor axis " + hv);
    }
}
