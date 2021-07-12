import {IParcel} from "./parcel.model";

export interface IAuth {
  email: string,
  password: string
}

export interface IUser {
  id?: number;
  first_name: string;
  last_name: string;
  email: string;
  password: string
  registered_on: string
  role: string
}
