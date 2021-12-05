using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawn : MonoBehaviour
{
	Avatar avatar;          //  avatar ������Ʈ
	public float speed;     //  �ɾ�� �ӵ�
	public float aspeed;    //  ȸ���ӵ�
	public float direction; //  z���� �������� �ؼ� �ð�������� ��ŭ ȸ���ؼ� �ٶ󺸴� ����
	GameObject nameGo;      //  �̸��ǿ� ���ӿ�����Ʈ
	public string joinItem; //  ���� ������ ���� ������

	void Start()
	{
	}
	void Update()
	{
		//  1. avatar�� ���� ���ٸ� �ƹ��͵� ���ϵ��� �Ѵ�.
		if(avatar == null) return;

		//  2. frame �ð��� ���ɴϴ�.
		var t = Time.deltaTime;

		//  3. �ִϸ��̼� ����
		if(speed > 0.0f) avatar.Walk();
		else if(avatar.GetAnimation() == 1) avatar.Stand();

		//  4. ȸ�� �̵�
		direction += t*aspeed;
		avatar.transform.localEulerAngles = new Vector3(0, direction, 0);

		//  5. ��ġ �̵�
		var rad = direction * Mathf.PI / 180.0f;
		var dirv = new Vector3(Mathf.Sin(rad), 0, Mathf.Cos(rad));
		avatar.transform.localPosition += dirv*t*speed;

		//  6. �̸����� �׻� ī�޶� �ٶ󺸵��� ȸ���Ѵ�.(Billboard ����)
		nameGo.transform.LookAt(nameGo.transform.position + 
			Camera.main.transform.rotation*Vector3.forward,
			Camera.main.transform.rotation*Vector3.up);
}

	//  ���� �� ������ �ƹ�Ÿ�� ���´�.
	public Avatar GetAvatar() { return avatar; }

	//  �ƹ�Ÿ�� �����Ѵ�.
	public void CreateAvatar(string name, int model)
	{
		//  1. �ƹ�Ÿ�� �����Ѵ�.
		avatar = gameObject.AddComponent<Avatar>();
		avatar.Create(model);
		
		//  2. �̸��� �����
		nameGo = new GameObject("Text");
		var nameText = nameGo.AddComponent<TextMesh>();
		nameText.text = name;

		//  3. �ƹ�Ÿ ������Ʈ�� �̸��� ���̱�
		nameGo.transform.parent = gameObject.transform;
		nameGo.transform.localPosition = new Vector3(0, 1.9f, 0);
		nameGo.transform.localScale = new Vector3(0.15f, 0.15f, 0.15f);
		nameText.anchor = TextAnchor.MiddleCenter;
	}

	//  �ƹ�Ÿ�� ���� �����Ѵ�.
	public void ChangeLook(int hair, int body, int legs, int shoes)
	{
		avatar.ChangeLook(hair, body, legs, shoes);
	}
}
