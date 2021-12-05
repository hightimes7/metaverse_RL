using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawn : MonoBehaviour
{
	Avatar avatar;          //  avatar 오브젝트
	public float speed;     //  걸어가는 속도
	public float aspeed;    //  회전속도
	public float direction; //  z축을 기준으로 해서 시계방향으로 얼만큼 회전해서 바라보는 방향
	GameObject nameGo;      //  이름판용 게임오브젝트
	public string joinItem; //  현재 참여한 월드 아이템

	void Start()
	{
	}
	void Update()
	{
		//  1. avatar가 현재 없다면 아무것도 안하도록 한다.
		if(avatar == null) return;

		//  2. frame 시간을 얻어옵니다.
		var t = Time.deltaTime;

		//  3. 애니메이션 적용
		if(speed > 0.0f) avatar.Walk();
		else if(avatar.GetAnimation() == 1) avatar.Stand();

		//  4. 회전 이동
		direction += t*aspeed;
		avatar.transform.localEulerAngles = new Vector3(0, direction, 0);

		//  5. 위치 이동
		var rad = direction * Mathf.PI / 180.0f;
		var dirv = new Vector3(Mathf.Sin(rad), 0, Mathf.Cos(rad));
		avatar.transform.localPosition += dirv*t*speed;

		//  6. 이름판이 항상 카메라를 바라보도록 회전한다.(Billboard 구현)
		nameGo.transform.LookAt(nameGo.transform.position + 
			Camera.main.transform.rotation*Vector3.forward,
			Camera.main.transform.rotation*Vector3.up);
}

	//  현재 이 스폰의 아바타를 얻어온다.
	public Avatar GetAvatar() { return avatar; }

	//  아바타를 생성한다.
	public void CreateAvatar(string name, int model)
	{
		//  1. 아바타를 생성한다.
		avatar = gameObject.AddComponent<Avatar>();
		avatar.Create(model);
		
		//  2. 이름판 만들기
		nameGo = new GameObject("Text");
		var nameText = nameGo.AddComponent<TextMesh>();
		nameText.text = name;

		//  3. 아바타 오브젝트에 이름판 붙이기
		nameGo.transform.parent = gameObject.transform;
		nameGo.transform.localPosition = new Vector3(0, 1.9f, 0);
		nameGo.transform.localScale = new Vector3(0.15f, 0.15f, 0.15f);
		nameText.anchor = TextAnchor.MiddleCenter;
	}

	//  아바타의 옷을 변경한다.
	public void ChangeLook(int hair, int body, int legs, int shoes)
	{
		avatar.ChangeLook(hair, body, legs, shoes);
	}
}
