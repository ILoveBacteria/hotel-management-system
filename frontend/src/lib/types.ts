export interface GuestProfile {
  phone_number: string;
  avatar: string;
  national_id: string;
  address: string;
}

export interface UserProfile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  username: string;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean;
  guest_profile: GuestProfile;
}

export interface Reserve {
  id: number;
  price: number;
  check_in: string;
  check_out: string;
  status: "registered" | "canceled" | "paid" | "check-in" | "check-out";
  created_at: string;
  updated_at: string;
  user: number;
  room: number;
}

export interface Room {
  room_number: number;
  is_active: boolean;
  status: "available" | "occupied" | "maintenance";
  last_maintained: string | null;
  room_type: number;
}

export interface RoomType {
  id: number;
  name: string;
  price: number;
  double_beds: number;
  single_beds: number;
  description: string;
}

export interface RoomImage {
  id: number;
  caption: string;
  image: string;
  uploaded_at: string;
  is_primary: boolean;
  room_type: number;
}

export interface Bill {
  id: number;
  reserve: string;
  amount: number;
  status: "waiting" | "paid" | "overdue";
  due_date: string;
  payment_date: string | null;
  created_at: string;
  updated_at: string;
}
