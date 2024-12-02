// src/lib/types.ts
export interface Booking {
    id: string;
    roomNumber: string;
    checkIn: string;
    checkOut: string;
    status: 'Confirmed' | 'Pending' | 'Checked In';
}

export interface HotelEvent {
    name: string;
    date: string;
    time: string;
    location: string;
    status: string;
}

export interface Service {
    type: 'cleaning' | 'roomService' | 'maintenance';
    date: string;
    time: string;
    roomNumber: string;
    status: string;
}


export interface Room {
    id: string;
    number: string;
    type: string;
    capacity: number;
    bedType: string;
    pricePerNight: number;
    sqft: number;
    amenities: string[];
    description: string;
    imageUrl?: string;
    images?: string[];
    status: 'available' | 'occupied' | 'maintenance';
}