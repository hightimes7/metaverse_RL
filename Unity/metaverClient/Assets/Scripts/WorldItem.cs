using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WorldItem : MonoBehaviour
{
	Material[] mtlList;
	Material mtlBoard;
	void Awake()
	{
		mtlList = new Material[3];
		mtlList[1] = Resources.Load("Materials/White") as Material;
		mtlList[2] = Resources.Load("Materials/Black") as Material;
		mtlBoard = Resources.Load("Materials/Board", typeof(Material)) as Material;
	}
	void Update()
	{
	}
	public bool CreateItem(string itemName, float x, float y, float dir)
	{
		if(itemName == "Reversi") CreateReversi(transform);
		else
		{
			//  1. item을 사용할 게임오브젝트를 생성합니다.
			var item = GameObject.CreatePrimitive(PrimitiveType.Cube);
			//  2. 생성한 아이템을 현재 오브젝트의 자식으로 등록합니다.
			item.transform.parent = transform;
			item.name = "0";
		}
		name = itemName;
		//  3. 위치를 지정합니다.
		transform.localPosition = new Vector3(x, 0, y);
		transform.localEulerAngles = new Vector3(0, dir, 0);
		return true;
	}
	void CreateReversi(Transform transform)
	{
		//  리버시의 8x8 판을 만듭니다.
		for(int i = 0; i < 8; i++)
		{
			for(int j = 0; j < 8; j++)
			{
				var go = GameObject.CreatePrimitive(PrimitiveType.Cube);
				go.transform.localScale = new Vector3(0.19f, 1, 0.19f);
				go.transform.localPosition = new Vector3(0.2f*j-0.8f, 0.0f, 0.2f*i-0.8f);
				go.transform.parent = transform;
				var rend = go.GetComponent<Renderer>();
				rend.material = mtlBoard;
				go.name = string.Format("{0}", i*8+j);
				go = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
				go.transform.localScale = new Vector3(0.18f, 0.05f, 0.18f);
				go.transform.localPosition = new Vector3(0.2f*j-0.8f, 0.5f, 0.2f*i-0.8f);
				go.transform.parent = transform;
				go.name = string.Format("c{0}", i*8+j);
				go.SetActive(false);
			}
		}
	}
	public void ActionItem(string name, string cmd, string data)
	{
		if(name != "Reversi") return;
		if(cmd == "place")
		{
			if(data == "fail")
				Debug.Log("Placing is failed");
			else
				UpdateItem(name, data);
		}
		else if(cmd == "join") Debug.LogFormat("Join Reversi with {0}.", data);
	}
	public void UpdateItem(string name, string data)
	{
		if(name != "Reversi") return;
		for(int i = 0; i < transform.childCount; i++)
		{
			var t = transform.GetChild(i);
			if(t.name[0] == 'c')
			{
				var idx = int.Parse(t.name.Substring(1));
				if(data[idx] == '1') 
				{
					t.gameObject.SetActive(true);
					var rend = t.gameObject.GetComponent<Renderer>();
					rend.material = mtlList[1];
				}
				else if(data[idx] == '2')
				{
					t.gameObject.SetActive(true);
					var rend = t.gameObject.GetComponent<Renderer>();
					rend.material = mtlList[2];
				}
				else
				{
					t.gameObject.SetActive(false);
				}
			}
		}
	}
}
