package com.demo.entry;

import lombok.Data;

import java.io.Serializable;

@Data
public class User implements Serializable {
    private String userId;
    private String name;

    public User(String userId, String name) {
        this.userId = userId;
        this.name = name;
    }
}
