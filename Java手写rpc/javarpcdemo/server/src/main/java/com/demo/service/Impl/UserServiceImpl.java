package com.demo.service.Impl;

import com.demo.entry.User;
import com.demo.service.UserService;

public class UserServiceImpl implements UserService {

    @Override
    public User getUserById(String userId) {
        return new User(userId, "name: "+userId);
    }
}
