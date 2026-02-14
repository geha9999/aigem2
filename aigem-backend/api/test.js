export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  res.status(200).json({
    status: 'OK',
    message: 'AIGEM2 Backend API is running',
    timestamp: new Date().toISOString(),
    endpoints: [
      'POST /api/activation/request',
      'POST /api/activation/verify-email',
      'POST /api/license/activate',
      'POST /api/license/heartbeat'
    ]
  })
}