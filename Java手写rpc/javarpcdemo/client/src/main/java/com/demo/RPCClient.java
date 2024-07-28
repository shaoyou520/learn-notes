package com.demo;

import com.demo.entry.User;
import com.demo.service.ClientProxy;
import com.demo.service.UserService;

public class RPCClient {
    public static void main(String[] args) {
        try {
            ClientProxy clientProxy = new ClientProxy("127.0.0.1", 8899);
            UserService userService = clientProxy.getProxy(UserService.class);
            User user = userService.getUserById("99");
            System.out.println("服务端返回的User:"+user);
            user = userService.getUserById("100");
            System.out.println("服务端返回的User:"+user);

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("客户端启动失败");
        }
    }
}
