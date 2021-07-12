import {ITeller} from "./tellers.model";

export interface IParcel {
  id?: number,
  sender: ISender,
  receiver: IReceiver,
  teller: ITeller,
  item: string,
  dispatch_date: string,
  delivered_date: string,
  arrival_date: string,
  cost: number,
  quantity: number,
  delivered: boolean
}

export interface ISender {
  id?: number,
  full_name: string,
  phone: string,
  email: string,
  center: string,
}

export interface IReceiver {
  id?: number,
  full_name: string,
  phone: string,
  email: string,
  center: string,
}
