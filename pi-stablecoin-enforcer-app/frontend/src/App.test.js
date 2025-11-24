import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import App from './App';

// Mock dependencies
jest.mock('axios');
jest.mock('stellar-sdk', () => ({
  Server: jest.fn(() => ({
    loadAccount: jest.fn().mockResolvedValue({}),
    submitTransaction: jest.fn().mockResolvedValue({ hash: 'test-hash' }),
    transactions: jest.fn(() => ({
      forAccount: jest.fn(() => ({
        limit: jest.fn(() => ({
          call: jest.fn().mockResolvedValue({ records: [{ hash: 'tx1', created_at: '2023-01-01' }] })
        }))
      }))
    }))
  })),
  Keypair: { fromSecret: jest.fn(() => ({})) },
  TransactionBuilder: jest.fn(() => ({
    addOperation: jest.fn().mockReturnThis(),
    setTimeout: jest.fn().mockReturnThis(),
    build: jest.fn(() => ({ sign: jest.fn() }))
  })),
  Networks: { TESTNET: 'testnet' },
  Operation: { invokeContractFunction: jest.fn() }
}));
jest.mock('@stellar/freighter-api', () => ({
  Freighter: {
    connect: jest.fn().mockResolvedValue({ address: 'test-account' })
  }
}));

describe('Pi Coin Enforcer Super App', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({ data: [{ institution: 'IOSCO', is_certified: true, score: 95 }] });
    axios.post.mockResolvedValue({ data: { valid: true, result: 'enforced' } });
  });

  test('renders app title and connect button', () => {
    render(<App />);
    expect(screen.getByText('Pi Coin Stablecoin Enforcer Super App')).toBeInTheDocument();
    expect(screen.getByText('Connect Freighter Wallet')).toBeInTheDocument();
  });

  test('connects wallet successfully', async () => {
    render(<App />);
    const connectButton = screen.getByText('Connect Freighter Wallet');
    fireEvent.click(connectButton);
    
    await waitFor(() => {
      expect(screen.getByText('Account: test-account')).toBeInTheDocument();
    });
  });

  test('enforces Pi Coin successfully', async () => {
    render(<App />);
    // Mock connected account
    const connectButton = screen.getByText('Connect Freighter Wallet');
    fireEvent.click(connectButton);
    await waitFor(() => screen.getByText('Account: test-account'));
    
    // Fill form
    fireEvent.change(screen.getByPlaceholderText('Value (314159)'), { target: { value: '314159' } });
    fireEvent.change(screen.getByDisplayValue('mining'), { target: { value: 'mining' } });
    fireEvent.change(screen.getByDisplayValue('USDC'), { target: { value: 'USDC' } });
    
    const enforceButton = screen.getByText('Enforce Pi Coin');
    fireEvent.click(enforceButton);
    
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/enforce', expect.any(Object));
      expect(screen.getByText('Pi Coin Enforced Successfully!')).toBeInTheDocument(); // Assume alert mock
    });
  });

  test('handles enforcement error', async () => {
    axios.post.mockRejectedValue(new Error('AI Rejected'));
    render(<App />);
    
    // Connect and enforce
    const connectButton = screen.getByText('Connect Freighter Wallet');
    fireEvent.click(connectButton);
    await waitFor(() => screen.getByText('Account: test-account'));
    
    fireEvent.change(screen.getByPlaceholderText('Value (314159)'), { target: { value: '314159' } });
    const enforceButton = screen.getByText('Enforce Pi Coin');
    fireEvent.click(enforceButton);
    
    await waitFor(() => {
      expect(screen.getByText('Enforcement failed: AI Rejected')).toBeInTheDocument();
    });
  });

  test('loads compliance badges', async () => {
    render(<App />);
    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/badges');
      expect(screen.getByText('IOSCO')).toBeInTheDocument();
    });
  });

  test('loads transaction history', async () => {
    render(<App />);
    // Mock account connected
    const connectButton = screen.getByText('Connect Freighter Wallet');
    fireEvent.click(connectButton);
    await waitFor(() => screen.getByText('Account: test-account'));
    
    await waitFor(() => {
      expect(screen.getByText('Hash: tx1')).toBeInTheDocument();
    });
  });

  test('evolves system', async () => {
    render(<App />);
    const evolveButton = screen.getByText('Evolve System');
    fireEvent.click(evolveButton);
    
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/evolve');
      expect(screen.getByText('System Evolved!')).toBeInTheDocument(); // Assume alert mock
    });
  });

  test('displays quantum security status', () => {
    render(<App />);
    expect(screen.getByText('Quantum Secure: Yes')).toBeInTheDocument();
  });

  test('shows error for unconnected wallet enforcement', () => {
    render(<App />);
    const enforceButton = screen.getByText('Enforce Pi Coin');
    fireEvent.click(enforceButton);
    
    expect(screen.getByText('Connect wallet first')).toBeInTheDocument();
  });
});

// Mock global alert for tests
global.alert = jest.fn();
