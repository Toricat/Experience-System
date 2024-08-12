// src/helpers/authSchemas.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email("Địa chỉ email không hợp lệ"),
  password: z.string().min(6 , "Mật khẩu phải có ít nhất 6 ký tự"),
});

export const registerSchema = z.object({
  email: z.string().email("Địa chỉ email không hợp lệ"),
  password: z.string().min(6,"Mật khẩu phải có ít nhất 6 ký tự"),
  name: z.string().min(2,"Tên phải có nhất 2 ký tự"),
  // 
});
