using UnityEngine;
using UnityEngine.UI;
using System.Text;
using System.Collections.Generic;

public class Main : MonoBehaviour
{
	enum CameraMode {
		FirstView,			//	1인칭 시점
		TrackView,			//	3인칭 시점
		CameraModeMax
	};
	//	Current camera mode
	CameraMode camMode = CameraMode.TrackView;
	//	First view mode camera parameters
	float xAngle=0;			//	카메라가 보고있는 각도
	float yAngle=0;			//	카메라가 보고있는 각도
	//	Track view mode camera paramters
	float distance = 5.0f;  //  camera distance
	float zoom;             //  camera zoom
	float camoffset;        //  camera offset angle

	Vector2 lastMousePos;   //  last mouse position
	SocketDesc socketDesc;  //  소켓 디스크립터

	Dictionary<string, Spawn> spawns;
	Spawn mySpawn;          //  본인의 스폰
	Dictionary<string, WorldItem> worldItems;
	GameObject messageBox;
	GameObject toastMessage;
	float toastMessageRemain;

	void Start()
	{
		//  소켓 디스크립터를 생성합니다.
		socketDesc = SocketDesc.Create();

		//  spawn들을 관리할 spawns를 생성합니다.
		spawns = new Dictionary<string, Spawn>();
		//  world item들을 관리할 worldItems를 생성합니다.
		worldItems = new Dictionary<string, WorldItem>();

		//	MessageBox를 찾습니다.
		messageBox = GameObject.Find("MessageBox").gameObject;
		//	MessageBox를 안 보이도록 hiding합니다.
		messageBox.SetActive(false);

		//	ToastMessage를 찾습니다.
		toastMessage = GameObject.Find("ToastMessage").gameObject;
		//	ToastMessage를 안 보이도록 hiding합니다.
		toastMessage.SetActive(false);
		//	ToastMessage 남은 시간을 -1.0으로 초기화합니다.
		toastMessageRemain = -1.0f;
	}
	void Update()
	{
		//  현재 스폰이 생성되어 있지 않았다면 아무 작업 안 하도록 합니다.
		if(mySpawn == null) return;

		//  W키가 눌리면 전진
		if(Input.GetKeyDown(KeyCode.W)) { mySpawn.speed = 1.0f; SendMove(); }
		else if(Input.GetKeyUp(KeyCode.W)) { mySpawn.speed = 0.0f; SendMove(); }
		if(Input.GetKeyDown(KeyCode.S)) { mySpawn.speed = -0.5f; SendMove(); }
		else if(Input.GetKeyUp(KeyCode.S)) { mySpawn.speed = 0.0f; SendMove(); }
		//  A키가 눌리면 좌회전, D키가 눌리면 우회전
		//  t 변수에 한 프레임의 시간 (초단위)를 저장
		if(Input.GetKeyDown(KeyCode.A)) { mySpawn.aspeed = -90.0f; SendMove(); }
		else if(Input.GetKeyUp(KeyCode.A)) { mySpawn.aspeed = 0.0f; SendMove(); }
		if(Input.GetKeyDown(KeyCode.D)) { mySpawn.aspeed = 90.0f; SendMove(); }
		else if(Input.GetKeyUp(KeyCode.D)) { mySpawn.aspeed = 0.0f; SendMove(); }
		
		//  마우스 휠 값을 읽어와서 zoom에 적용
		zoom += Input.mouseScrollDelta.y*0.1f;
		if(zoom<-1.0f) zoom = -1.0f; else if(zoom > 1.0f) zoom = 1.0f;
		var t = Time.deltaTime;

		//  마우스 버튼 0 또는 마우스 버튼 1이 눌리면 마우스의 위치를 표시
		if(Input.GetMouseButtonDown(0) || Input.GetMouseButtonDown(1))
		{
			//  1. 카메라 위치로부터 해당 마우스 위치로 가는 ray 생성
			var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
			//  2. 해당 ray를 이용하여 충돌검사
			RaycastHit hit;
			if(Physics.Raycast(ray, out hit))
			{
				Transform ht = hit.transform;
				WorldItem wi = null;
				while( ht != null )
				{
					if(ht.gameObject.TryGetComponent<WorldItem>(out wi)) break;
					ht = ht.parent;
				}
				if(wi != null)
				{
					Debug.LogFormat("Hit : {0}", wi.name);
					//  마우스 버튼 0이 눌렸으면 place 수행, 1이 눌렸으면 해당 아이템에 join
					if(Input.GetMouseButtonDown(0))
					{
						var mesg = string.Format("action {0} {1} place {2}", 
							mySpawn.name, wi.name, hit.transform.name);
						socketDesc.Send(Encoding.UTF8.GetBytes(mesg));
					}
					else if(mySpawn.joinItem == wi.name)
					{
						var mesg = string.Format("{0}에서 떠나시겠습니까?", wi.name);
						var yesMesg = string.Format("action {0} {1} leave", 
							mySpawn.name, wi.name);
						ShowMessageBox(mesg, yesMesg);
					}
					else
					{
						var mesg = string.Format("{0}에 참여하시겠습니까?", wi.name);
						var yesMesg = string.Format("action {0} {1} join", 
							mySpawn.name, wi.name);
						ShowMessageBox(mesg, yesMesg);
					}
				}
			}
		}
		
		if(camMode == CameraMode.FirstView) UpdateFirstView();
		else UpdateTrackView();

		//	toastMessage 시간 검사
		if(toastMessageRemain > 0.0f)
		{
			//	1. 현재 프레임 타임만큼 시간만큼 남은 시간을 없앤다.
			toastMessageRemain -= Time.deltaTime;

			//	2. 남은시간이 0이하이면, 시간이 모두 흐른 것이므로 toastMessage를 사라지게 한다.
			if(toastMessageRemain <= 0.0f) toastMessage.SetActive(false);
		}
	}
	void FixedUpdate()
	{
		//  1. 소켓 디스크립터가 존재하지 않으면 아무짓도 안하기
		if(socketDesc == null) return;
		//  2. processNetwork이 true가 아니라면 아무짓도 안하기
		if(!socketDesc.ProcessNetwork()) return;
		//  3. 패킷 가져오기
		var packet = Encoding.UTF8.GetString(socketDesc.GetPacket());
		Debug.Log(packet);
		var ss = packet.Split();
		if(ss[0] == "join")
		{
			if(!spawns.ContainsKey(ss[1]))
			{
				var go = new GameObject();
				var spawn = go.AddComponent<Spawn>();
				spawns[ss[1]] = spawn;

				//	새로운 플레이어가 접속했다고 메세지를 토스트에 뿌립니다.
				var mesg = string.Format("친구 {0}이 접속했습니다.\n안녕하세요.", ss[1]);
				ShowToastMessage(mesg);
			}
		}
		else if(ss[0] == "leave")
		{
			if(spawns.ContainsKey(ss[1]))
			{
				var go = spawns[ss[1]].gameObject;
				GameObject.Destroy(go);
				spawns.Remove(ss[1]);
			}
		}
		else if(ss[0] == "avatar")
		{
			if(spawns.ContainsKey(ss[1]))
			{
				var spawn = spawns[ss[1]];
				if(spawn != mySpawn) spawn.CreateAvatar(ss[1], int.Parse(ss[2]));
			}
		}
		else if(ss[0] == "look")
		{
			if(spawns.ContainsKey(ss[1]))
			{
				var spawn = spawns[ss[1]];
				spawn.ChangeLook(int.Parse(ss[2]), int.Parse(ss[3]), int.Parse(ss[4]), int.Parse(ss[5]));
			}
		}
		else if(ss[0] == "worlddata")
		{
			//  1. 새로운 게임오브젝트 생성
			var go = new GameObject();
			//  2. 이 오브젝트를 WorldItem 컴포넌트를 등록
			var wi = go.AddComponent<WorldItem>();
			//  3. 실제 오브젝트를 생성
			wi.CreateItem(ss[1], float.Parse(ss[2]), float.Parse(ss[3]), float.Parse(ss[4]));
			//  4. worldItems라는 자료구조에 해당 월드 아이템을 등록
			worldItems[ss[1]] = wi;
		}
		else if(ss[0] == "update")
		{
			//  1. 이름을 가지고 worlditems 항목을 찾아봅니다.
			if(worldItems.ContainsKey(ss[1]))
			{
				//  2. 찾은 항목에서 UpdateItem 함수를 호출합니다.
				var wi = worldItems[ss[1]];
				wi.UpdateItem(ss[1], ss[2]);
			}
		}
		else if(ss[0] == "action")
		{
			//  1. 이름을 가지고 worlditems 항목을 찾아봅니다.
			if(worldItems.ContainsKey(ss[2]))
			{
				Debug.LogFormat("action : {0}, {1}", ss[1], ss[3]);
				//  2. 찾은 항목에서 UpdateItem 함수를 호출합니다.
				var wi = worldItems[ss[2]];
				//	3. 만약 world item에 join하는 명령어인 경우 해당 캐릭터를 앉도록 한다.
				if(ss[4] == "join")
				{
					var spawn = spawns[ss[1]];
					spawn.GetAvatar().Sit();
					//	현재 스폰이 ss[2]에 참여했음을 표시
					spawn.joinItem = ss[2];
					//	토스트 메세지 표시
					var mesg = string.Format("{0}가 {1}에 참여했습니다.", ss[1], ss[2]);
					ShowToastMessage(mesg);
				}
				else if(ss[4] == "leave")
				{
					var spawn = spawns[ss[1]];
					spawn.GetAvatar().Stand();
					//	현재 스폰이 ss[2]에서 떠났음을 표시
					spawn.joinItem = null;
					//	토스트 메세지 표시
					var mesg = string.Format("{0}가 {1}에 떠났습니다.", ss[1], ss[2]);
					ShowToastMessage(mesg);
				}
				else if(ss[4] == "quit")
				{
					var mesg = string.Format("경기 종료. 백 : {0}, 흑 : {1}", ss[5], ss[6]);
					ShowToastMessage(mesg);
				}
				wi.ActionItem(ss[1], ss[2], ss[3]);
			}
		}
		else if(ss[0] == "move")
		{
			if(spawns.ContainsKey(ss[1]))
			{
				 var spawn = spawns[ss[1]];
				 // myspawn이 아닌 경우에만 설정
				 if(spawn != mySpawn)
				 {
					spawn.transform.localPosition = new Vector3(float.Parse(ss[2]), 0.0f, float.Parse(ss[3]));
					spawn.direction = float.Parse(ss[4]);
					spawn.speed = float.Parse(ss[5]);
					spawn.aspeed = float.Parse(ss[6]);
					Debug.LogFormat("spawn : {0}, speed = {1}, aspeed = {2}", ss[2], spawn.speed, spawn.aspeed);
				 }
			}
		}
	}
	void UpdateFirstView()
	{
		//	만약 c키가 눌리면 카메라 모드를 트랙 뷰로 바꿉니다.
		if(Input.GetKeyUp(KeyCode.C))
		{
			camMode = CameraMode.TrackView;
			return;
		}
		//	마우스 버튼 1이 클릭된 상태에서 팬 처리
		if(Input.GetMouseButtonDown(1)) lastMousePos = Input.mousePosition;
		else if(Input.GetMouseButtonUp(1)) lastMousePos = Vector2.zero;
		//	lastMousePos값이 0벡터가 아닌 경우에는 팬 처리
		if(lastMousePos != Vector2.zero)
		{
			xAngle -= Input.mousePosition.y - lastMousePos.y;
			yAngle += Input.mousePosition.x - lastMousePos.x;
			if(xAngle < -45.0f) xAngle = -45.0f;
			else if(xAngle > 45.0f) xAngle = 45.0f;
			if(yAngle < -90.0f) yAngle = -90.0f;
			else if(yAngle > 90.0f) yAngle = 90.0f;
			lastMousePos = Input.mousePosition;
		}
		//	카메라 위치 설정
		Camera.main.transform.localPosition = mySpawn.transform.localPosition +
			new Vector3(0.0f, 1.7f, 0.0f);
		var dir = mySpawn.transform.localEulerAngles;
		Camera.main.transform.localEulerAngles = new Vector3(
			dir.x + xAngle, dir.y + yAngle, dir.z);
	}
	void UpdateTrackView()
	{
		//	만약 c키가 눌리면 카메라 모드를 일인칭 뷰로 바꿉니다.
		if(Input.GetKeyUp(KeyCode.C))
		{
			camMode = CameraMode.FirstView;
			return;
		}
		//  마우스 버튼 1이 클릭된 상태에서 팬 처리
		if(Input.GetMouseButtonDown(1)) lastMousePos = Input.mousePosition;
		else if(Input.GetMouseButtonUp(1)) lastMousePos = Vector2.zero;
		if(lastMousePos != Vector2.zero)
		{
			camoffset += Input.mousePosition.x - lastMousePos.x;
			lastMousePos = Input.mousePosition;
		}
		else if(mySpawn.speed != 0.0f)
		{
			if(camoffset < 0.0f)
			{
				camoffset += 0.1f;
				if(camoffset > 0.0f) camoffset = 0.0f;
			}
			else if(camoffset > 0.0f)
			{
				camoffset -= 0.1f;
				if(camoffset < 0.0f) camoffset = 0.0f;
			}
		}
		//  카메라 위치
		var camd = distance*Mathf.Pow(2.0f, zoom);
		var rad = Mathf.Deg2Rad * (mySpawn.direction+camoffset);
		var cdirv = new Vector3(Mathf.Sin(rad), 0, Mathf.Cos(rad));
		Camera.main.transform.localPosition = mySpawn.transform.localPosition - 
			cdirv*camd*Mathf.Cos(30*Mathf.PI/180.0f) + 
			(new Vector3(0, camd*Mathf.Sin(30*Mathf.PI/180.0f)+1.8f, 0));
		Camera.main.transform.localEulerAngles = new Vector3(30.0f, (mySpawn.direction+camoffset), 0);
	}
	//  접속 버튼이 눌렸을 때의 작업
	public void OnButtonConnect()
	{
		//  1. Find "LoginWindow"
		var loginWindow = GameObject.Find("LoginWindow");
		//  2. Find "InputField"
		var name = loginWindow.transform.Find("InputField").GetComponent<InputField>();
		//  3. Print result
		Debug.LogFormat("Connet with {0}.", name.text);
		//  4. Hide Login window
		loginWindow.SetActive(false);

		//  Spawn 만들기
		//  1. Make a Empty Game object
		var go = new GameObject(name.text);
		//  2. Avatar component 추가하기
		mySpawn = go.AddComponent<Spawn>();
		//  3. Avatar 생성하기
		var model = Random.Range(0, 2);
		mySpawn.CreateAvatar(name.text, model);
		var hair = Random.Range(0, 4);
		var body = Random.Range(0, 4);
		var legs = Random.Range(0, 4);
		var shoes = Random.Range(0, 4);
		mySpawn.ChangeLook(hair, body, legs, shoes);

		//  접속하기
		if(socketDesc.Connect("127.0.0.1", 8888))
		{
			Debug.Log("Connected");
			socketDesc.Send(Encoding.UTF8.GetBytes(string.Format("join {0}", name.text)));
			socketDesc.Send(Encoding.UTF8.GetBytes(string.Format("avatar {0} {1}", name.text, model)));
			socketDesc.Send(Encoding.UTF8.GetBytes(string.Format("look {0} {1} {2} {3} {4}", 
				name.text, hair, body, legs, shoes)));
			spawns[name.text] = mySpawn;
		}
		else
		{
			Debug.LogError("Connection is failed");
		}
	}

	string yesSendMesg;			//	yes 버튼이 눌릴 경우 전달할 메세지
	//	Message Box를 보이도록 합니다.
	public void ShowMessageBox(string mesg, string yes)
	{
		//	1. MessageBox를 보이도록 합니다.
		messageBox.SetActive(true);

		//	2. Message 오브젝트를 찾습니다.
		var messageObj = messageBox.transform.Find("Message").GetComponent<Text>();

		//	3. Message 오브젝트에 mesg값을 적습니다.
		messageObj.text = mesg;

		//	4. yes 버튼이 눌릴 경우 전달할 메세지를 저장합니다.
		yesSendMesg = yes;
	}

	//	ToastMessage를 보이도록 합니다.
	public void ShowToastMessage(string mesg, float duration = 5.0f)
	{
		//	1. ToastMessage를 보이도록 합니다.
		toastMessage.SetActive(true);

		//	2. Message 오브젝트를 찾습니다.
		var messageObj = toastMessage.transform.Find("Message").GetComponent<Text>();

		//	3. Message 오브젝트에 mesg값을 적습니다.
		messageObj.text = mesg;

		//	4. 보이는 시간을 기록합니다.
		toastMessageRemain = duration;
	}

	//	Yes 버튼이 눌린 경우
	public void OnButtonYes()
	{
		//	1. MessageBox를 숨기도록 합니다.
		messageBox.SetActive(false);

		//	2. action userName Reversi join
		if(yesSendMesg != null) socketDesc.Send(Encoding.UTF8.GetBytes(yesSendMesg));
	}
	//	No 버튼이 눌린 경우
	public void OnButtonNo()
	{
		//	1. MessageBox를 숨기도록 합니다.
		messageBox.SetActive(false);
	}
	void SendMove()
	{
		var mesg = string.Format("move {0} {1} {2} {3} {4} {5}",
			mySpawn.name, mySpawn.transform.localPosition.x, mySpawn.transform.localPosition.z,
			mySpawn.direction, mySpawn.speed, mySpawn.aspeed);
		socketDesc.Send(Encoding.UTF8.GetBytes(mesg));
	}
}
