using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Motor : MonoBehaviour
{
    public KeyCode cw, ccw;
    public float speed = 5.0f;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(cw)) transform.Rotate(Time.deltaTime*speed, 0, 0);
        else if (Input.GetKey(ccw)) transform.Rotate(-Time.deltaTime*speed, 0, 0);
    }
}
