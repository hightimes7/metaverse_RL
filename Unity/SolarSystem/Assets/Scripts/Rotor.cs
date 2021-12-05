using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotor : MonoBehaviour
{
    float GlobalAngleSpeed = 0.1f;
    // 회전하는 속도. 초당 몇도가 회전할건가? 1.0은 1초에 1도
    public float AngleSpeed = 1.0f;
        
    // Update is called once per frame
    void Update()
    {
        // 1) 이전 프레임에서 지금 프레임까지의 시간(delta time)을 이용해서
        //     y축 기준으로 회전할 각도를 계산
        //    Time.deltaTime = 이전프레임에서 지금프레임까지 걸린 시간(초단위)
        var yangle = Time.deltaTime * AngleSpeed * GlobalAngleSpeed;
        // 2) y축을 기준으로 yangle 만큼 회전하도록 함
        transform.Rotate(0.0f, yangle, 0.0f);        
    }
}
