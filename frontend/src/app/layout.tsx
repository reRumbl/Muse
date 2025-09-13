import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import Link from 'next/link';
import './globals.css';


const geistSans = Geist({
    variable: '--font-geist-sans',
    subsets: ['latin'],
});


const geistMono = Geist_Mono({
    variable: '--font-geist-mono',
    subsets: ['latin'],
});


export const metadata: Metadata = {
    title: 'Muse',
    description: 'Music shop',
};


export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang='ru'>
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased`}
            >
                <header className='bg-gray-800 text-white p-4'>
                    <nav className='container mx-auto flex justify-between'>
                        <Link href='/' className='text-xl font-bold'>
                            Muse
                        </Link>
                        <div>
                            <Link href='/ensembles' className='mr-4'>
                                Ensembles
                            </Link>
                        </div>
                    </nav>
                </header>
                <main>{children}</main>
            </body>
        </html>
    );
}
