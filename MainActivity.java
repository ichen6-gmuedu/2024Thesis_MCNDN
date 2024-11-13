package com.example.phone;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import com.example.phone.databinding.ActivityMainBinding;
import android.annotation.SuppressLint;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.net.NetworkInterface;
import java.util.List;
import java.util.Collections;
import android.content.Context;
import java.util.Formatter;
import android.text.method.ScrollingMovementMethod;



public class MainActivity extends AppCompatActivity {
    ServerSocket serverSocket;
    Thread Thread1 = null;
    TextView tvIP, tvPort, tvConnectionStatus;
    TextView tvMessages;
    Button btnSend;
    public static String SERVER_IP = "";
    public static final int SERVER_PORT = 9095;
    String message;
    private ActivityMainBinding binding;
    public int testCounter = 0;
    public boolean connectedflag = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tvIP = findViewById(R.id.tvIP);
        tvPort = findViewById(R.id.tvPort);
        tvConnectionStatus = findViewById(R.id.tvConnectionStatus);
        tvMessages = findViewById(R.id.tvMessages);
        tvMessages.setMovementMethod(new ScrollingMovementMethod());
        btnSend = findViewById(R.id.btnSend);

        try {
            SERVER_IP = getLocalIpAddress();

        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            serverSocket = new ServerSocket(SERVER_PORT);
        } catch (IOException e) {
        e.printStackTrace();
        }

        Thread1 = new Thread(new Thread1());
        Thread1.start();
        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(connectedflag) {
                    new Thread(new Thread3(message)).start();
                }
            }
        });

    }

    private String getLocalIpAddress() throws UnknownHostException {
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager != null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int ipInt = wifiInfo.getIpAddress();

        if (ipInt == 0){
            try {
                List<NetworkInterface> interfaces = Collections.list(NetworkInterface.getNetworkInterfaces());
                for (NetworkInterface intf : interfaces) {
                    List<InetAddress> addrs = Collections.list(intf.getInetAddresses());
                    for (InetAddress addr : addrs) {
                        if (!addr.isLoopbackAddress()) {
                            return  addr.getHostAddress();
                        }
                    }
                }
            } catch (Exception ex) { } // for now eat exceptions
            return "";
        } else return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(ipInt).array()).getHostAddress();



    }
    private PrintWriter output;
    private InputStream input;
    private Socket socket;
    class Thread1 implements Runnable {
        @Override
        public void run() {
            //Socket socket;
            try {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        tvIP.setText("IP: " + SERVER_IP);
                        tvPort.setText("Port: " + String.valueOf(SERVER_PORT));
                        tvConnectionStatus.setText("Not connected\n");
                        connectedflag = false;
                    }
                });
                try {

                    // connect to python client
                    socket = serverSocket.accept();
                    output = new PrintWriter(socket.getOutputStream());
                    input = socket.getInputStream();

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            connectedflag = true;
                            tvConnectionStatus.setText("Connected\n");
                        }
                    });
                    new Thread(new Thread2()).start();
                } catch (IOException e) {
                    e.printStackTrace();
                    tvMessages.append(e.toString());
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    private class Thread2 implements Runnable {
        @Override
        public void run() {
            while (true) {
                try {


                    byte[] buffer = new byte[1024];
                    int read;
                    while((read = input.read(buffer)) != -1) {

                        String message = new String(buffer, 0, read);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                tvMessages.append("Received data:" + message + "\n");
                            }
                        });
                    }
                    Thread1 = new Thread(new Thread1());
                    Thread1.start();
                    return;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
    class Thread3 implements Runnable {
        private String message;
        Thread3(String message) {
            this.message = message;
        }
        @Override
        public void run() {
            String interestPacket = "VA/Fairfax/GMU/CS/actionOn:1R153AN";
            output.write(interestPacket);
            output.flush();
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    tvMessages.append("\nTest counter: " + Integer.toString(testCounter) + "\n");
                    testCounter ++;
                    tvMessages.append("Interest Packet: " + interestPacket + "\n");
                }
            });
        }
    }

}






