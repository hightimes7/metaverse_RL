using System;
using System.Text;
using System.Net.Sockets;
using UnityEngine;

public class SocketDesc
{
    // ��Ʈ��ũ ���¸� ���� ������
    enum NetworkState
    {
        Disconnect,     // ���� ��Ʈ��ũ�� ������ �� �� ����
        Ready,          // ������ �Ǿ �޼����� ���� �� �ִ� ����
        WaitForHeader,  // ���� ����� �а� �ִ� ��
        WaitForMessage, // ���� �޼����� �а� �ִ� ��
        Complete,       // �޼��� ������ ������
        MaxNumber
    }

    // ����� ������
    Socket socket;      // ��Ʈ��ũ ������ ���� ��Ʈ��ũ �ڵ�
    byte[] packet;      // ��Ʈ��ũ �޼��� ��Ŷ
    byte[] recvBuffer;  // �ӽ÷� ������ ����
    NetworkState state; // ��Ʈ��ũ ����

    // ���� ��ũ���� ���� �Լ�
    public static SocketDesc Create()
    {
        // 1. ������ ����
        Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        if (sock == null) return null;
        // 2. ���� ��ũ���͸� ����
        var desc = new SocketDesc();
        desc.socket = sock;
        desc.recvBuffer = new byte[4];
        // 3. ���� ��ũ���͸� ��ȯ
        return desc;
    }

    // ��Ʈ��ũ ����
    public bool Connect(string address, int port)
    {
        // 1. ���� ���� ���°� ��������� �ƴϸ�
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

    // ��Ʈ��ũ ����� ����
    public void Shutdown()
    {
        if (socket == null || !socket.Connected) return;
        socket.Shutdown(SocketShutdown.Both);
    }

    // ��Ʈ��ũ���� ���۵� �����͸� ��������
    public byte[] GetPacket()
    {
        // 1. ������ �Ϸ�� ��쿡�� packet�� ��ȯ
        if (state == NetworkState.Complete)
        {
            state = NetworkState.Ready;
            return packet;
        }
        return null;
    }

    // ��Ʈ��ũ ó���ϱ�
    public bool ProcessNetwork()
    {
        // 1. ������ ���ų� �񿬰������ ��� false ��ȯ
        if (socket == null || !socket.Connected) return false;
        // 2. ������ �Ϸ�� ��쿡�� �ƹ� �ϵ� �� �ϱ�
        if (state == NetworkState.Complete) return true;
        // 3. Ready �����̸� ����� �б�
        if(state == NetworkState.Ready)
        {
            state = NetworkState.WaitForHeader;
            socket.BeginReceive(recvBuffer, 0, 4, SocketFlags.None,
                new AsyncCallback(ReceiveComplete), null);
        }
        return false;
    }

    // ������ �Ϸ�� ��� �Ҹ��� �ݹ� �Լ�
    void ReceiveComplete(IAsyncResult ar)
    {
        int len = socket.EndReceive(ar);
        // len�� 0�� ��쿡�� ����ʿ��� ������ ���� ���
        // len�� 0���� ���� ��쿡�� ��Ʈ��ũ ������ �߻��� ���
        if(len <= 0) { socket.Close(); state = NetworkState.Disconnect; return; }
        // ��Ʈ��ũ ���°� ����� ��ٸ��� ���
        if(state == NetworkState.WaitForHeader)
        {
            // 1. ����Ʈ ��Ʈ���� ���ڿ��� ��ȯ
            string str = Encoding.UTF8.GetString(recvBuffer);
            // 2. ���ڿ��� ������ ��ȯ
            int needed = Int32.Parse(str);
            // 3. needed ��ŭ ���۸� ����
            packet = new byte[needed];
            // 4. ��Ʈ��ũ ���¸� �޼����� ��ٸ��� ������ ��ȯ
            state = NetworkState.WaitForMessage;
            // 5. ��Ʈ��ũ �б� ��û�ϱ�
            socket.BeginReceive(packet, 0, needed, SocketFlags.None,
                new AsyncCallback(ReceiveComplete), null);
        }
        else if(state == NetworkState.WaitForMessage)
        {
            // 1. ��Ʈ��ũ ���¸� �Ϸ��� �ٲߴϴ�.
            state = NetworkState.Complete;
        }
    }

    // ��Ŷ ���� ������
    public void Send(byte[] packet)
    {
        string str = String.Format("{0,4}", packet.Length);
        byte[] sendBuffer = new byte[4 + packet.Length];
        System.Buffer.BlockCopy(Encoding.UTF8.GetBytes(str), 0, sendBuffer, 0, 4);
        System.Buffer.BlockCopy(packet, 0, sendBuffer, 4, packet.Length);
        socket.BeginSend(sendBuffer, 0, 4 + packet.Length, SocketFlags.None,
            new AsyncCallback(SendComplete), null);
    }

    // ������ �Ϸ�Ǿ��� �� �Ҹ��� �ݹ��Լ�
    void SendComplete(IAsyncResult ar)
    {
        socket.EndSend(ar);
    }
}
