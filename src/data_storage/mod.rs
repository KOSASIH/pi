pub mod data_storage;

use rust_crypto::aes::Aes128;
use rust_crypto::block_modes::{BlockMode, Cbc};
use rust_crypto::buffer::{BufferResult, ReadBuffer, WriteBuffer};
use std::fs;
use tokio::fs as async_fs;

type Aes128Cbc = Cbc<Aes128>;

pub struct DataStorage {
    key: [u8; 16], // Encryption key
}

impl DataStorage {
    pub fn new() -> Self {
        Self { key: [0; 16] } // In production, use secure key generation
    }

    pub async fn store_data(&self, filename: &str, data: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
        let iv = [0u8; 16]; // Initialization vector
        let cipher = Aes128Cbc::new_var(&self.key, &iv)?;
        let mut buffer = [0u8; 1024];
        let mut read_buffer = ReadBuffer::new(data);
        let mut write_buffer = WriteBuffer::new(&mut buffer);
        loop {
            let result = cipher.encrypt(&mut read_buffer, &mut write_buffer, true)?;
            match result {
                BufferResult::BufferUnderflow => break,
                BufferResult::BufferOverflow => {}
            }
        }
        async_fs::write(filename, &buffer[..write_buffer.position()]).await?;
        println!("Encrypted data stored: {}", filename);
        Ok(())
    }

    pub async fn retrieve_data(&self, filename: &str) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
        let encrypted = async_fs::read(filename).await?;
        let iv = [0u8; 16];
        let cipher = Aes128Cbc::new_var(&self.key, &iv)?;
        let mut buffer = vec![0u8; encrypted.len()];
        let mut read_buffer = ReadBuffer::new(&encrypted);
        let mut write_buffer = WriteBuffer::new(&mut buffer);
        cipher.decrypt(&mut read_buffer, &mut write_buffer, true)?;
        Ok(buffer[..write_buffer.position()].to_vec())
    }

    pub async fn backup(&self, filename: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Autonomous backup to Pi Network (simulate)
        let data = self.retrieve_data(filename).await?;
        async_fs::write(&format!("backup_{}", filename), &data).await?;
        println!("Backup created for: {}", filename);
        Ok(())
    }
}
