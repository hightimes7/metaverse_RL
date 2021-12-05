using System;
using System.Text;
using System.Net.Sockets;
using UnityEngine;

public class SocketDesc
{
    // 네트워크 상태를 위한 열거형
    enum NetworkState
    {
        Disconnect,     // 현재 네트워크는 연결이 안 됨 상태
        Ready,          // 연결이 되어서 메세지를 받을 수 있는 상태
        WaitForHeader,  // 현재 헤더를 읽고 있는 중
        WaitForMessage, // 현재 메세지를 읽고 있는 중
        Complete,       // 메세지 수신이 끝났음
        MaxNumber
    }

    // 사용할 변수들
    Socket socket;      // 네트워크 접속을 위한 네트워크 핸들
    byte[] packet;      // 네트워크 메세지 패킷
    byte[] recvBuffer;  // 임시로 저장할 버퍼
    NetworkState state; // 네트워크 상태

    // 소켓 디스크립터 생성 함서
    public static SocketDesc Create()
    {
        // 1. 소켓을 생성
        Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        if (sock == null) return null;
        // 2. 소켓 디스크립터를 생성
        var desc = new SocketDesc();
        desc.socket = sock;
        desc.recvBuffer = new byte[4];
        // 3. 소켓 디스크립터를 반환
        return desc;
    }

    // 네트워크 접속
    public bool Connect(string address, int port)
    {
        // 1. 현재 접속 상태가 연결끊김이 아니면
        if (state != NetworkState.Disconnect) socket.Close();
        try { socket.Connect(address, port); }
        catch (SocketException e)
        {
            Debug.LogFormat("Error in connect : {0}", e.Message);
            return false;
        }
        state = NetworkState.Ready;
        return socket.Connected;
    }

    // 네트워크 통신을 종료
    public void Shutdown()
    {
        if (socket == null || !socket.Connected) return;
        socket.Shutdown(SocketShutdown.Both);
    }

    // 네트워크에서 전송된 데이터를 가져오기
    public byte[] GetPacket()
    {
        // 1. 전송이 완료된 경우에는 packet을 반환
        if (state == NetworkState.Complete)
        {
            state = NetworkState.Ready;
            return packet;
        }
        return null;
    }

    // 네트워크 처리하기
    public bool ProcessNetwork()
    {
        // 1. 소켓이 없거나 비연결상태인 경우 false 반환
        if (socket == null || !socket.Connected) return false;
        // 2. 전송이 완료된 경우에는 아무 일도 안 하기
        if (state == NetworkState.Complete) return true;
        // 3. Ready 상태이면 헤더를 읽기
        if(state == NetworkState.Ready)
        {
            state = NetworkState.WaitForHeader;
            socket.BeginReceive(recvBuffer, 0, 4, SocketFlags.None,
                new AsyncCallback(ReceiveComplete), null);
        }
        return false;
    }

    // 전송이 완료된 경우 불리는 콜백 함수
    void ReceiveComplete(IAsyncResult ar)
    {
        int len = socket.EndReceive(ar);
        // len이 0인 경우에는 상대쪽에서 접속을 끊은 경우
        // len이 0보다 작은 경우에는 네트워크 에러가 발생한 경우
        if(len <= 0) { socket.Close(); state = NetworkState.Disconnect; return; }
        // 네트워크 상태가 헤더를 기다리는 경우
        if(state == NetworkState.WaitForHeader)
        {
            // 1. 바이트 스트링을 문자열로 변환
            string str = Encoding.UTF8.GetString(recvBuffer);
            // 2. 문자열을 정수로 변환
            int needed = Int32.Parse(str);
            // 3. needed 만큼 버퍼를 생성
            packet = new byte[needed];
            // 4. 네트워크 상태를 메세지를 기다리는 것으로 전환
            state = NetworkState.WaitForMessage;
            // 5. 네트워크 읽기 요청하기
            socket.BeginReceive(packet, 0, needed, SocketFlags.None,
                new AsyncCallback(ReceiveComplete), null);
        }
        else if(state == NetworkState.WaitForMessage)
        {
            // 1. 네트워크 상태를 완료라고 바꿉니다.
            state = NetworkState.Complete;
        }
    }

    // 패킷 내용 보내기
    public void Send(byte[] packet)
    {
        string str = String.Format("{0,4}", packet.Length);
        byte[] sendBuffer = new byte[4 + packet.Length];
        System.Buffer.BlockCopy(Encoding.UTF8.GetBytes(str), 0, sendBuffer, 0, 4);
        System.Buffer.BlockCopy(packet, 0, sendBuffer, 4, packet.Length);
        socket.BeginSend(sendBuffer, 0, 4 + packet.Length, SocketFlags.None,
            new AsyncCallback(SendComplete), null);
    }

    // 전송이 완료되었을 때 불리는 콜백함수
    void SendComplete(IAsyncResult ar)
    {
        socket.EndSend(ar);
    }
}
