using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotor : MonoBehaviour
{
    float GlobalAngleSpeed = 0.1f;
    // ȸ���ϴ� �ӵ�. �ʴ� ��� ȸ���Ұǰ�? 1.0�� 1�ʿ� 1��
    public float AngleSpeed = 1.0f;
        
    // Update is called once per frame
    void Update()
    {
        // 1) ���� �����ӿ��� ���� �����ӱ����� �ð�(delta time)�� �̿��ؼ�
        //     y�� �������� ȸ���� ������ ���
        //    Time.deltaTime = ���������ӿ��� ���������ӱ��� �ɸ� �ð�(�ʴ���)
        var yangle = Time.deltaTime * AngleSpeed * GlobalAngleSpeed;
        // 2) y���� �������� yangle ��ŭ ȸ���ϵ��� ��
        transform.Rotate(0.0f, yangle, 0.0f);        
    }
}
